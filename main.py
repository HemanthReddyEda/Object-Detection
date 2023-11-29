import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import json
def detect_objects():
 image_path = image_path_entry.get()
 image = cv2.imread(image_path)
 labelsPath = "C:/Users/ehred/object-detection-system/yolo-coco/coco.names"
 LABELS = open(labelsPath).read().strip().split("\n")
 COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
 weightsPath = "C:/Users/ehred/object-detection-system/yolo-coco/yolov3 .weights"
 configPath = "C:/Users/ehred/object-detection-system/yolo-coco/yolov3.cfg"
 net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
 image = cv2.imread(image_path)
 (H, W) = image.shape[:2]
 ln = net.getLayerNames()
 out_layer_indices = net.getUnconnectedOutLayers()
 print("Output Layer Indices:", out_layer_indices)
 ln = [ln[i - 1] for i in out_layer_indices]
19
 blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
 net.setInput(blob)
 layerOutputs = net.forward(ln)
 boxes = []
 confidences = []
 classIDs = []
 for output in layerOutputs:
 for detection in output:
 scores = detection[5:]
 classID = np.argmax(scores)
 confidence = scores[classID]
 if confidence > 0.5: # You can adjust the confidence threshold as needed
 box = detection[0:4] * np.array([W, H, W, H])
 (centerX, centerY, width, height) = box.astype("int")
 x = int(centerX - (width / 2))
 y = int(centerY - (height / 2))
 boxes.append([x, y, int(width), int(height)])
 confidences.append(float(confidence))
 classIDs.append(classID)
 idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3) # You can adjust the thresholds
 if len(idxs) > 0:
 for i in idxs.flatten():
 (x, y) = (boxes[i][0], boxes[i][1])
 (w, h) = (boxes[i][2], boxes[i][3])
20
 color = [int(c) for c in COLORS[classIDs[i]]] # Note the closing parenthesis on this line
 cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
 text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
 cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
 cv2.imshow("Image", image)
 cv2.waitKey(0)
 result_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 result_image = Image.fromarray(result_image)
 result_image = ImageTk.PhotoImage(result_image)
 result_label.config(image=result_image)
 result_label.image = result_image
user_credentials = {
 "user1": "password1",
 "user2": "password2",
}
def load_user_credentials():
 global user_credentials
 try:
 with open("user_credentials.json", "r") as file:
 user_credentials = json.load(file)
 except FileNotFoundError:
 user_credentials = {}
load_user_credentials()
def check_credentials():
 username = username_entry.get()
 password = password_entry.get()
 if username in user_credentials and user_credentials[username] == password:
 messagebox.showinfo("Login", "Login successful")
21
 login_frame.grid_forget() # Hide login frame after successful login
 detect_frame.grid(row=0, column=0, sticky="nsew") # Show object detection frame
 else:
 messagebox.showerror("Login Error", "Invalid username or password")
def register_user():
 new_username = new_username_entry.get()
 new_password = new_password_entry.get()
 if new_username and new_password:
 user_credentials[new_username] = new_password
 with open("user_credentials.json", "w") as file:
 json.dump(user_credentials, file)
 messagebox.showinfo("Registration", "Registration successful")
 registration_frame.pack_forget() # Hide registration frame after successful registration
 login_frame.pack() # Show login frame
 new_username_entry.delete(0, 'end')
 new_password_entry.delete(0, 'end')
 else:
 messagebox.showerror("Registration Error", "Please enter a valid username and password")
root = tk.Tk()
root.title("Object Detection GUI")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
login_frame = tk.Frame(root, bg="lightblue")
login_frame.grid(row=0, column=0, sticky="nsew")
registration_frame = tk.Frame(root, bg="lightblue")
registration_frame.grid(row=0, column=0, sticky="nsew")
detect_frame = tk.Frame(root, bg="lightblue")
detect_frame.grid(row=0, column=0, sticky="nsew")
image_path_label = tk.Label(detect_frame, text="Enter Image Path:")
image_path_label.grid(row=0, column=0, columnspan=2)
image_path_entry = tk.Entry(detect_frame)
image_path_entry.grid(row=1, column=0, columnspan=2)
22
browse_button = tk.Button(detect_frame, text="Upload Image",
 command=lambda: image_path_entry.insert(0, filedialog.askopenfilename()))
browse_button.grid(row=2, column=0, columnspan=2)
detect_button = tk.Button(detect_frame, text="Detect Objects", command=detect_objects)
detect_button.grid(row=3, column=0, columnspan=2)
result_label = tk.Label(detect_frame)
result_label.grid(row=4, column=0, columnspan=2)
login_label = tk.Label(login_frame, text="Login", font=("Arial", 24))
login_label.grid(row=0, column=0, columnspan=2)
username_label = tk.Label(login_frame, text="Username:")
username_label.grid(row=1, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=1, column=1)
password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=2, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=2, column=1)
login_button = tk.Button(login_frame, text="Login", command=check_credentials)
login_button.grid(row=3, column=0, columnspan=2)
register_label = tk.Label(login_frame, text="Don't have an account? Register here:")
register_label.grid(row=4, column=0, columnspan=2)
register_button = tk.Button(login_frame, text="Register", command=lambda:
(login_frame.grid_forget(), registration_frame.grid(row=0, column=0, sticky="nsew")))
register_button.grid(row=5, column=0, columnspan=2)
registration_label = tk.Label(registration_frame, text="Register")
registration_label.grid(row=0, column=0, columnspan=2)
new_username_label = tk.Label(registration_frame, text="New Username:")
new_username_label.grid(row=1, column=0)
new_username_entry = tk.Entry(registration_frame)
new_username_entry.grid(row=1, column=1)
new_password_label = tk.Label(registration_frame, text="New Password:")
new_password_label.grid(row=2, column=0)
new_password_entry = tk.Entry(registration_frame, show="*")
23
new_password_entry.grid(row=2, column=1)
register_button = tk.Button(registration_frame, text="Register", command=register_user)
register_button.grid(row=3, column=0, columnspan=2)
detect_frame.grid_forget()
registration_frame.grid_forget()
root.mainloop()
