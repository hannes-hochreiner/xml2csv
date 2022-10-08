import xml.etree.ElementTree as ET
import os
import sys

def remove_namespace(tag):
  return tag[tag.rfind('}') + 1:]

def process_file(input_filename, output_filename):
  print(f'processing "{input_filename}"... writing output to "{output_filename}"')
  tree = ET.parse(input_filename)
  root = tree.getroot()
  output_file = open(output_filename, mode='w', encoding='utf-8')

  fields = []

  for entry in root[0][0]:
    fields.append(remove_namespace(entry.tag))

  # print("|".join(fields))
  output_file.write("|".join(fields) + "\n")

  for entry in root[0]:
    index = 0
    values = []  

    for field in entry:
      tag = remove_namespace(field.tag)

      if fields[index] != tag:
        raise Exception(f'expected field "{fields[index]}" found field "{tag}"')

      text = "" if field.text is None else field.text

      values.append(text)
      index += 1

    # print("|".join(values))
    output_file.write("|".join(values) + "\n")

def process_dir(in_dir, out_dir):
  files = os.listdir(in_dir)

  for file in files:
    if not file.endswith('.xml'):
      break

    input_filename = os.path.join(in_dir, file)
    output_filename = os.path.join(out_dir, file[:-3] + "csv")

    if os.path.isfile(input_filename):
      process_file(input_filename, output_filename)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    raise Exception('usage "python main.py <input_dir> <output_dir>')

  process_dir(sys.argv[1], sys.argv[2])