import cv2
import dlib
import glob
import os
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import tkinter


class MainWindow(object):
    def __init__(self, phase, start=1):
        self.root = tkinter.Tk()
        self.root.title("Data Annotator")
        self.dlib = dlib.cnn_face_detection_model_v1(os.path.join(Path(__file__).parent, "mmod_human_face_detector.dat"))
        self.file = phase + ".txt"
        self.index = start - 1
        self.onclick = 0
        self.phase = phase
        self.label_map = {"Anger": 0, "Angry": 0, "Disgust": 1, "Fear": 2,
                          "Happy": 3, "Neutral": 4, "Sad": 5, "Surprise": 6}
        self.data = self.load_data()
        self.add_components()
        self.set_layout()
        self.get_item(self.index)
        self.render()

    def read_file(self):
        self.record = [line.rstrip('\n') for line in open(self.file)]
        pass

    def load_data(self):
        data = {}
        items = []
        path = os.path.join(Path(__file__).parent.parent, 'data', "CAER-S", self.phase)
        labels = os.listdir(path)
        for label in labels:
            if os.path.isfile(os.path.join(path, label)):
                labels.remove(label)
        for label in labels:
                data[label] = []
                folder = os.path.join(path, label)
                for image in glob.glob(os.path.join(folder, "*.png")):
                    data[label].append(image)
        for label, images in data.items():
                images.sort()
                for image in images:
                    items.append([image, label])
        return items

    def add_components(self):
        self.img_label = tkinter.Label(self.root)
        self.img_label.bind("<Button>", self.bbox_callback)
        self.path_label = tkinter.Label(self.root)
        self.size_label = tkinter.Label(self.root)
        self.cat_label = tkinter.Label(self.root)
        self.bbox_label = tkinter.Label(self.root)
        self.save_btn = tkinter.Button(
            self.root, text="save", command=self.save_callback)
        self.back_btn = tkinter.Button(
            self.root, text="back", command=self.back_callback)
        self.next_btn = tkinter.Button(
            self.root, text="next", command=self.next_callback)

    def set_layout(self):
        self.img_label.grid(row=0, column=0, columnspan=3)
        self.path_label.grid(row=1, column=0)
        self.size_label.grid(row=1, column=1)
        self.cat_label.grid(row=1, column=2)
        self.bbox_label.grid(row=2, column=0)
        self.back_btn.grid(row=3, column=0, sticky=tkinter.W)
        self.next_btn.grid(row=3, column=1, sticky=tkinter.W)
        self.save_btn.grid(row=3, column=2, sticky=tkinter.W)

    def render(self):
        self.img_label.configure(image=self.img)
        self.path_label.configure(text=self.path)
        self.size_label.configure(
            text=str(self.size[0]) + " X " + str(self.size[1]))
        self.cat_label.configure(text=self.label)
        self.bbox_label.configure(text="lefttop=("+str(self.bbox_lefttop[0])+","+str(
            self.bbox_lefttop[1])+") | rightbottom=("+str(self.bbox_rightbottom[0])+","+str(self.bbox_rightbottom[1])+")")

    def get_item(self, index):
        self.read_file()
        if index + 1 > len(self.record):
            root_path = os.path.join(Path(__file__).parent.parent, 'data', 'CAER-S')
            self.path = self.data[index][0].replace(root_path+"/", "")
            self.label = self.data[index][1]
            img = Image.open(self.data[index][0])
            img_cv = cv2.imread(self.data[index][0])
            result = self.dlib(img_cv, 2)
            max_confidence = -100
            final_rect = None
            for rect in result:
                if rect.confidence > max_confidence:
                    max_confidence = rect.confidence
                    final_rect = rect.rect
            if final_rect:
                x1 = final_rect.left()
                y1 = final_rect.top()
                x2 = final_rect.right()
                y2 = final_rect.bottom()
            else:
                x1 = 0
                y1 = 0
                x2 = 0
                y2 = 0
        else:
            sample = self.record[index].split(",")
            self.path, x1, y1, x2, y2 = sample[0], int(sample[2]), int(sample[3]), int(sample[4]), int(sample[5])
            root_path = os.path.join(Path(__file__).parent.parent, 'data', 'CAER-S')
            img = Image.open(os.path.join(root_path, self.path))
            for label, id in self.label_map.items():
                if id == int(sample[1]):
                    self.label = label
                    break
        self.size = img.size
        draw = ImageDraw.Draw(img)
        draw.rectangle([x1, y1, x2, y2])
        del draw
        self.img = ImageTk.PhotoImage(img)
        img.close()

        self.bbox_lefttop, self.bbox_rightbottom = (x1, y1), (x2, y2)

    def bbox_callback(self, event):
        self.onclick += 1
        if self.onclick % 2 == 1:
            self.bbox_lefttop = event.x, event.y
        else:
            self.bbox_rightbottom = event.x, event.y
        self.render()

    def save_callback(self):

        lines = [line for line in open(self.file)]
        if self.index + 1 > len(lines):
            content = ",".join([self.path, str(self.label_map[self.label])] + [str(v) for v in self.bbox_lefttop] + [
                           str(v) for v in self.bbox_rightbottom]) + "\n"
            lines.append(content)
        else:
            line = lines[self.index]
            content = ",".join(line.split(",")[:-4] + [str(v) for v in self.bbox_lefttop] + [
                           str(v) for v in self.bbox_rightbottom]) + "\n"
            lines[self.index] = content
        f = open(self.file, mode="w")
        f.writelines(lines)
        f.close()

    def back_callback(self):
        if self.index > 0:
            self.index -= 1
            self.get_item(self.index)
            self.render()
            print(self.index+1)

    def next_callback(self):
        self.index += 1
        self.get_item(self.index)
        self.render()
        self.save_callback()
        print(self.index+1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow(phase="test", start=1)
    app.run()
