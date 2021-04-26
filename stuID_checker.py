from pdf2image import convert_from_path
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import numpy as np
import argparse
import csv
import cv2
import sys
import os

SUBMODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'submodules', 'OMRChecker'))
sys.path.append(SUBMODULE_DIR)
from extension import ExtensionManager
from template import Template
import config
import utils

def write_csv(rows, output_path):
  with open(output_path, 'w') as csvfile:
    out_writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
      out_writer.writerow(row)

def rename_docs(results, input_dir):
  for result in results:
    filename = result[0]
    stu_id = result[1]
    src_path = input_dir / filename 
    dst_path = (input_dir / stu_id)
    if dst_path.with_suffix('.pdf').exists(): # check and resolve filename conflicts
      print(f'{dst_path}.pdf already exists!')
      dst_path /= '_' + datetime.now().strftime("%Y%m%d%H%M%S%f")
    dst_path = dst_path.with_suffix('.pdf')
    try:
      os.rename(src_path, dst_path)
    except:
      print(f'Failed to rename from {src_path} to {dst_path}!')

def filter_filenames(directory, extensions=('*.pdf','*.PDF')):
  return sorted([f for ext in extensions for f in directory.glob(ext)])

def format_response(template, omrResp):
  csvResp = {}
  UNMARKED_SYMBOL = ''
  for qNo, respKeys in template.concats.items():
    csvResp[qNo] = ''.join([omrResp.get(k, UNMARKED_SYMBOL)
                              for k in respKeys])
  for qNo in template.singles:
      csvResp[qNo] = omrResp.get(qNo, UNMARKED_SYMBOL)
  return csvResp

def get_result(omr_resp_dict, template):
  resp = format_response(template, omr_resp_dict)
  resp_cols = sorted(list(template.concats.keys()) + template.singles,
    key=lambda x: int(x[1:]) if ord(x[1]) in range(48, 58) else 0)
  return [resp[k] for k in resp_cols]

def process_omr(omr, template, filename):
  # Preprocess
  for pp in template.preprocessors:   # run preprocessors
    omr = pp.apply_filter(omr, None)           
  omr = utils.resize_util(omr,        # resize to conform to template
    config.uniform_width, config.uniform_height)
  
  omr_resp_dict = utils.readResponse(template, omr, name='')[0]
  return get_result(omr_resp_dict, template)

def process_dir(input_dir, output_path, template, rename, target_page=0):
  results = []
  for doc_filepath in tqdm(filter_filenames(input_dir)):
    doc_filename = doc_filepath.name
    omr = convert_from_path(doc_filepath, 400)[target_page] # extract target page from document
    omr = cv2.cvtColor(np.array(omr), cv2.COLOR_BGR2GRAY)   # convert to numpy and grayscale
    result = process_omr(omr, template, doc_filename)
    results.append([doc_filename] + result)
    print(result)

  try:
    write_csv(results, output_path)
    print(f'Results CSV written to {output_path}')
  except:
    print('CSV writing failed!')
  if rename:
    rename_docs(results, input_dir)

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("-i", "--input-dir", required=True, dest='input_dir', help="Specify an input directory.")
  argparser.add_argument("-o", "--output", default='outputs.csv', required=False, dest='output_path', help="Specify output path for the CSV.")
  argparser.add_argument("-p", "--page", default=0, type=int, dest='page', help="Specify the page to conduct OMR on.")
  argparser.add_argument("-r", "--rename",  action='store_true', dest='rename', help="Specify wether to rename documents based on their student numbers.")
  argparser.add_argument("-s", "--save-level", default=0, type=int, dest='save_level', help="Specify saveimglvl of OMRChecker.")
  args, unknown = argparser.parse_known_args()
  args = vars(args)
  if(len(unknown) > 0):
    print("\nError: Unknown arguments:", unknown)
    argparser.print_help()
    exit(11)

  # Process arugments
  ext_mgr = ExtensionManager(config.EXTENSION_PATH)
  template_path = Path(SUBMODULE_DIR) / 'samples' / 'sample5_fb_alignment' / 'template_fb_align.json'
  template = Template(template_path, ext_mgr.extensions)
  input_dir = Path(args['input_dir'])
  output_path = Path(args['output_path'])
  target_page = args['page']
  rename = args['rename']

  # Errors and warnings
  print(f'File renaming is set to {rename}.')
  if output_path.is_dir():
    raise ValueError('CSV output cannot be a directory!')

  # Procedure call
  config.saveimglvl = args['save_level']
  process_dir(input_dir, output_path, template, rename, target_page=target_page)

if __name__ == '__main__': main()