import json
import os

def labelme_to_paddleocr(labelme_json_dir, output_txt_path):
    with open(output_txt_path, 'w') as output_file:
        for root, dirs, files in os.walk(labelme_json_dir):
            for filename in files:
                json_path = os.path.join(root, filename)
                if filename.endswith('.json'):
                    with open(json_path, 'r',encoding='utf-8') as f:
                        data = json.load(f)
                        annotations = []
                        skip_file = False
                        for i in range(len(data["shapes"])):
                            label = data["shapes"][i]["label"][0:-2]
                            points = data["shapes"][i]["points"]
                            if len(points) != 2 and len(points) != 4:
                                skip_file = True
                                break
                            if len(points) == 2:
                                P00, P01 = points[0]  
                                P10, P11 = points[1]  
                                points = [[P00, P01], [P10, P01], [P10, P11], [P00, P11]]
                            elif len(points) == 4:
                                points = int,points
                            else :
                                continue
                            annotation = {
                                "transcription": label,
                                "points": points,
                                "difficult": False
                            }
                            annotations.append(annotation)
                        if skip_file:
                            continue
                        jpg_path = json_path.replace('.json','.jpg')
                        line = f"{jpg_path}\t{json.dumps(annotations, ensure_ascii=False)}\n"
                        output_file.write(line)

labelme_json_dir = ''
output_txt_path = ''
labelme_to_paddleocr(labelme_json_dir, output_txt_path)