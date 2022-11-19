
# A Gesture-based Tool for Sterile Browsing of Radiology Images

This project aims to build a hands-free digital image browsing system for use in a sterile setting in a medical environment.

## Quick Links

- [Project Repository](https://github.com/IBM-EPBL/IBM-Project-21974-1659800381)
- [Project Demonstration Video](https://drive.google.com/file/d/1wd168Ld-yCibywBhVcPSvzHZc-tcosIM/view?usp=sharing)
- [Project Report](./Final-Deliverables/Project-Report_PNT2022TMID53060.pdf)

## Team

- **Team ID:** PNT2022TMID53060
- **Project ID:** IBM-Project-21974-1659800381


| Role     | Name | Register Number |
| :-----------: | :-----------: | :------: |
| Team Leader | Karthik D | 195001047 | 
| Team Member 1 | A Anirudh | 195001015 |
| Team Member 2 | Nestor Ingarshal J | 195001069 | 
| Team Member 3 | Pugalarasu K  | 195001306 |

## Mentors

| Role | Name |
| :-----------: | :------: |
| Industry Mentor | Ms. Pradeepthi |
| Faculty Mentor | Lakshmi Priya S |

## Project Description

### Technology Used

- Artificial Intelligence
- Deep Learning
- Image Processing
- Web Development
- IBM Cloud Database

### Technology Stack

- Tensforflow/Keras
- OpenCV
- NumPy
- Flask
- NodeRED

### Motivation

Surgeons and doctors often require reference imaging results whilst operating on patients. Furthermore, they may need to manipulate the image view through basic tranformative operations such as panning, scaling, and rotation among others. However, in doing so, computer peripheral devices need to be accessed through touch. To avoid compromising the sterility of their instruments and operating hand, they presently instruct surgical assistants to operate the viewing media to adjust it to their requirement. The granularity in reaching their required state of the view is limited to the effectiveneess of the verbal communication, and can often take several attempts beefore reaching the required state. 

### Proposed Solution

To eliminate the need for such an assistant, and to make the manipulation operations more granular and completely in control of the surgeon/doctor, our system proposes to use gestures as the instruction media. The getures are captured through a camera attached to the viewing system; the digital frames are processed to recognize the gesture using deep learning; each gesture is mapped to a corresponding transformations on the image; and the transformation is effected on the image. This makes for a hands-free sterility-preserving view manipulation mechanism.

![data-flow-overview](./Project-Design-And-Planning/Project-Design-Phase-2/assets/Data-Flow-Overview.png)

### Implemented System

In practicality, the system's machine learning backend may be trained to recognize any number of gestures. For this proof-of-concept project, we implement 6 different gestures, and map them to specific operations on a medical image. The entire system is deployed on a web-server, with user-management, real-time gesture capturing, recognition and change effecting using peripherals commonly found on a typical personal computer: web-camera, LCD display and trackpad/mouse. 

![proposed-workflow](./Project-Design-And-Planning/Project-Design-Phase-1/assets/solution-architecture.png)
