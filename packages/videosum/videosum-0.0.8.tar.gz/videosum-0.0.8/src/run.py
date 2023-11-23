"""
@brief   Package to summarise a video into N frames. There are a lot of methods
         for video summarisation, and a lot of repositories in GitHub, but
         none of them seems to work out of the box. This package contains a 
         simple way of doing it.

@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    18 May 2022.
"""

import argparse
import imageio_ffmpeg
import numpy as np
import os
import cv2
import tqdm
import time
import multiprocessing
import logging

# My imports
import videosum


def help(short_option):
    """
    @returns The string with the help information for each command line option.
    """
    help_msg = {
        '-i': 'Path to the video (required: True)',
        '-o': 'Output directory path (required: True)',
        '-n': 'Number of frames in the collage (required: True)',
        '-x': 'Width of the collage (required: True)',
        '-y': 'Height of the collage (required: True)',
        '-a': 'Algorithm for frame selection, available options: time, frechet (required: True)',
        '-t': 'Add time segmentation based on the key frame selection (required: False)',
        '-f': 'Sampling frequency in fps (required: False)', 
        '-s': 'Time smoothing factor (required: False)',
        '-p': 'Number of processes (required: False)',
        '-l': 'Path to the log file (required: False)',
        '-m': 'Compute FID between storyboard and video (required: False)',
    }
    return help_msg[short_option]


def parse_cmdline_params():
    """@returns The argparse args object."""
    # Create command line parser
    parser = argparse.ArgumentParser(description='Easy-to-use video summarisation.')
    parser.add_argument('-i', '--input', required=True, type=str, 
                        help=help('-i'))
    parser.add_argument('-o', '--output', required=True, type=str, 
                        help=help('-o'))
    parser.add_argument('-n', '--nframes', required=True, type=int, 
                        help=help('-n'))
    parser.add_argument('-x', '--width', required=True, type=int, 
                        help=help('-x'))
    parser.add_argument('-y', '--height', required=True, type=int, 
                        help=help('-y'))
    parser.add_argument('-a', '--algo', required=True, type=str,
                        help=help('-a'))
    parser.add_argument('-t', '--time-segmentation', required=False, 
                        default=False, type=int, help=help('-t'))
    parser.add_argument('-f', '--fps', required=False, 
                        default=None, type=float, help=help('-f'))
    parser.add_argument('-s', '--time-smoothing', required=False, 
                        default=0., type=float, help=help('-s'))
    parser.add_argument('-p', '--processes', required=False,
                        default=multiprocessing.cpu_count(), type=int, 
                        help=help('-p'))
    parser.add_argument('-l', '--log', required=False, default='summary.log',
                        type=str, help=help('-l'))
    parser.add_argument('-m', '--metric', required=False, default=False,
                        type=bool, help=help('-m'))

    # Read parameters
    args = parser.parse_args()

    # Modify parameters according to needs
    args.time_segmentation = bool(args.time_segmentation)
    
    return args


def validate_cmdline_params(args):
    """
    @brief Input directory must exist and output must not.
    """
    if not os.path.isfile(args.input) and not os.path.isdir(args.input):
        raise RuntimeError('[ERROR] Input file or folder does not exist.')

    if os.path.isfile(args.output):
        raise RuntimeError('[ERROR] Output file already exists.')

    if args.algo not in videosum.VideoSummariser.ALGOS: 
        raise ValueError("[ERROR] The method {} does not exist.".format(args.algo))

    return args


def process_video(input_path, output_path, args):
    # Create video summariser
    vidsum = videosum.VideoSummariser(args.algo, args.nframes, 
                                      args.width, args.height, 
                                      time_segmentation=args.time_segmentation,
                                      fps=args.fps,
                                      time_smoothing=args.time_smoothing,
                                      compute_fid=args.metric)

    try:
        # Summarise video
        im = vidsum.summarise(input_path)

        # Save summary to the output folder
        cv2.imwrite(output_path, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    except IOError as e:
        logging.info("The video {} is broken. Skipping.".format(os.path.basename(input_path)))


def setup_logging(logfile_path):
    """
    @brief Sets up the logging to file.

    @param[in]  logfile_path  Path to the logfile, typically passed on in the
                              command line.
    """
    logging.basicConfig(filename=logfile_path, filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S', level=logging.DEBUG)


def main():
    # Read command line parameters
    args = parse_cmdline_params()
    validate_cmdline_params(args)

    # Setup logging
    setup_logging(args.log)
    
    # Check whether the input is a file or a folder of videos
    if os.path.isfile(args.input):
        # Create video summariser
        vidsum = videosum.VideoSummariser(args.algo, args.nframes, 
                                          args.width, args.height, 
                                          time_segmentation=args.time_segmentation,
                                          fps=args.fps, 
                                          time_smoothing=args.time_smoothing,
                                          compute_fid=args.metric)
        # The input is a file
        tic = time.time()
        im = vidsum.summarise(args.input)
        toc = time.time()
        print("[INFO] Video summarised in {} seconds.".format(toc - tic))
        cv2.imwrite(args.output, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    else:
        # The input is a folder of videos
        input_dir = args.input
        output_dir = args.output
        
        # Create output folder
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        # Gather the list of video filenames inside the folder
        videos = [x for x in os.listdir(input_dir) if x.endswith('.mp4')]
        prev_len = len(videos)

        # Filter out the videos that have been already summarised
        already_summarised = [x.split('.jpg')[0] + '.mp4' \
            for x in os.listdir(output_dir) if x.endswith('.jpg')]
        videos = [x for x in videos if x not in already_summarised] 
        print("[INFO] {} videos have been already summarised.".format(prev_len - len(videos)))
        
        # Build data input ready for batch processing
        data_inputs = []
        for v in videos:
            input_path = os.path.join(input_dir, v)
            output_path = os.path.join(output_dir, os.path.splitext(v)[0] + '.jpg')
            data_inputs.append((input_path, output_path, args))
        
        # Run batch processing
        pool = multiprocessing.Pool(processes=args.processes)
        pool.starmap(process_video, data_inputs)
        #for input_path, output_path, args in data_input:
        #    print("[INFO] Processing {} ...".format(input_path))
        #    process_video(input_path, output_path, args)


if __name__ == '__main__':
    main()
