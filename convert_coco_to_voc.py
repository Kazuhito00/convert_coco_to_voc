import os
import json
import argparse

import xmltodict
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert COCO annotation to Pascal VOC format.')

    parser.add_argument(
        'coco_file',
        help='COCO JSON file.',
        type=str,
    )
    parser.add_argument(
        'output_dir',
        help='Directory path to Pascal VOC file.',
        type=str,
    )

    parser.add_argument(
        '--set_name',
        help='train/test set name.',
        type=str,
        default='train',
    )
    parser.add_argument(
        '--bbox_offset',
        help='Bounding Box offset.',
        type=int,
        default=1,
    )

    parser.add_argument(
        '--folder',
        help='Base infomation:folder.',
        type=str,
        default='VOCCOCO',
    )
    parser.add_argument(
        '--path',
        help='Base infomation:path.',
        type=str,
        default='',
    )
    parser.add_argument(
        '--owner',
        help='Base infomation:owner name.',
        type=str,
        default='Unknown',
    )
    parser.add_argument(
        '--source_database',
        help='Base infomation:source database.',
        type=str,
        default='Unknown',
    )
    parser.add_argument(
        '--source_annotation',
        help='Base infomation:source annotation.',
        type=str,
        default='Unknown',
    )
    parser.add_argument(
        '--source_image',
        help='Base infomation:source image.',
        type=str,
        default='Unknown',
    )
    parser.add_argument(
        '--image_depth',
        help='Base infomation:image depth.',
        type=int,
        default=3,
    )
    parser.add_argument(
        '--segmented',
        help='Base infomation:segmented.',
        type=str,
        default='0',
    )

    args = parser.parse_args()

    return args


def main():
    # 引数取得
    args = get_args()

    coco_file = args.coco_file
    output_dir = args.output_dir

    set_name = args.set_name
    bbox_offset = args.bbox_offset

    folder = args.folder
    path = args.path
    owner = args.owner
    source_database = args.source_database
    source_annotation = args.source_annotation
    source_image = args.source_image
    image_depth = args.image_depth
    segmented = args.segmented

    # 出力対象ディレクトリパス
    output_dir = os.path.join(output_dir, folder)

    # 出力ディレクトリ生成
    output_dirs = {
        directory: os.path.join(output_dir, directory)
        for directory in ['Annotations', 'ImageSets', 'JPEGImages']
    }
    output_dirs['ImageSets'] = os.path.join(output_dirs['ImageSets'], 'Main')

    for _, directory in output_dirs.items():
        os.makedirs(directory, exist_ok=True)

    # COCO形式データ読み込み
    json_data = json.load(open(coco_file))

    # カテゴリーDict生成
    categories = {x['id']: x['name'] for x in json_data['categories']}

    # 画像情報Dict生成
    images = {}
    for image_info in tqdm(json_data['images'], 'Parse Images'):
        image_dict = create_image_dict(
            image_info['file_name'],
            image_info['width'],
            image_info['height'],
            image_depth,
            folder,
            path,
            owner,
            source_database,
            source_annotation,
            source_image,
            segmented,
        )
        images[image_info['id']] = image_dict

    # アノテーション情報Dict生成
    for annotation_info in tqdm(json_data['annotations'], 'Parse Annotations'):
        image_id = annotation_info['image_id']
        category_id = annotation_info['category_id']
        bbox = annotation_info['bbox']

        annotation_dict = create_object_dict(
            images[image_id]['annotation']['size'],
            categories[category_id],
            bbox,
            bbox_offset,
        )

        images[image_id]['annotation']['object'].append(annotation_dict)

    # Pascal VOC XML書き込み
    for key, image_info in tqdm(images.items(), 'Write Annotations'):
        image_info['annotation'][
            'object'] = image_info['annotation']['object'] or [None]

        xml_path = os.path.join(output_dirs['Annotations'],
                                '{}.xml'.format(str(key).zfill(12)))
        with open(xml_path, 'w') as fp:
            xmltodict.unparse(image_info, fp, full_document=False, pretty=True)

    # ファイル一覧テキスト書き込み
    txt_path = os.path.join(output_dirs['ImageSets'],
                            '{}.txt'.format(set_name))
    with open(txt_path, 'w') as fp:
        fp.writelines(
            list(map(lambda x: str(x).zfill(12) + '\n', images.keys())))

    print('Success: {}'.format(coco_file))


def create_image_dict(
    filename,
    width,
    height,
    depth=3,
    folder='VOC2012',
    path='',
    owner='Unknown',
    source_database='Unknown',
    source_annotation='Unknown',
    source_image='Unknown',
    segmented='0',
):
    image_dict = {
        'annotation': {
            'folder': folder,
            'filename': os.path.split(filename)[-1],
            'path': path,
            'owner': {
                'name': owner
            },
            'source': {
                'database': source_database,
                'annotation': source_annotation,
                'image': source_image
            },
            'size': {
                'width': width,
                'height': height,
                'depth': depth
            },
            'segmented': segmented,
            'object': []
        }
    }
    return image_dict


def create_object_dict(size_info, name, bbox, bbox_offset):
    x1, y1, w, h = bbox
    x2 = x1 + w
    y2 = y1 + h

    x1 = max(x1, 0) + bbox_offset
    y1 = max(y1, 0) + bbox_offset
    x2 = min(x2, size_info['width'])
    y2 = min(y2, size_info['height'])

    object_dict = {
        'name': name,
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': {
            'xmin': x1,
            'ymin': y1,
            'xmax': x2,
            'ymax': y2
        }
    }

    return object_dict


if __name__ == '__main__':
    main()
