from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import networkx as nx
from . Utils import insert_nodes, find_shortest_path, generate_directions,draw_path
from . models import *
from django.core.files.base import ContentFile
import base64
import os
from django.conf import settings



# Create your views here.
def home(request):
    return render(request, 'home.html')



def get_route(request):
    # Your existing code to generate image and directions
    image_path = r'static\assets\image.jpeg'  
    node_coordinates = [(38, 302),
                    (154, 206),
                    (194, 208),
                    (359, 204),
                    (389, 168),
                    (420, 207),
                    (585, 206),
                    (624, 208),
                    (764, 248),
                    (762, 309),
                    (732, 353),
                    (628, 354),
                    (596, 354),
                    (552, 334),
                    (506, 334),
                    (311, 331),
                    (247, 333),
                    (206, 352),
                    (165, 352),
                    (62, 352),
                    (92, 272),  # X1
                    (176, 273),  # X2
                    (275, 269),  # X3
                    (361, 269),  # X4
                    (393, 208),  # X5
                    (426, 279),  # X6
                    (520, 265),  # X7
                    (606, 277),
                    (696, 282)]  
    node_names = ['Library','Smart Class', 'Boys common room', 'Gents Toilet', 'Lift1', 'First aid room',
              'Lab House keeping','Kitchen', 'Restaurant', 'Classroom', 'Stairs near restaurant', 'Tutorial room',
              'Staff room', 'Stationary store', 'Class 205', 'Mini hall', 'Professors room', 'Pantry', 'Tutorial room1',
              'Stairs near Library', 'Near smart class', 'Near to smart class', 'Near Professors room', 'Near to the turning towards lift', 
              'Near lift', 'Near to lift', 'Near stationary ', 'Near kitchen','Near restaruant']

    img = insert_nodes(image_path, node_coordinates, node_names)

    # Your existing code to find shortest path and generate directions
    start_node_name = request.GET.get('start_node_name')
    end_node_name = request.GET.get('end_node_name')
    print(start_node_name)
    print(end_node_name)
    shortest_path_indices = find_shortest_path(node_coordinates, str(start_node_name), str(end_node_name))
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)

    # Draw the path on the image
    draw_path(img, shortest_path_indices, node_coordinates)

    # Serialize the image data
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Save the image data to the static files directory
    image_filename = f'navigation_image_{start_node_name}_{end_node_name}.jpg'  # Unique filename
    image_path = os.path.join(r"static", 'navigation_images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Print directions
    for direction in directions:
        print(direction)
    response_data = {
        "directions": directions,
        "image_filename": image_filename  # Include the image filename in the response
    }

    # Return JSON response
    return JsonResponse(response_data)



def preview(request):
    if request.method == "GET":
        start_node_name = request.GET.get('start_node_name')
        end_node_name = request.GET.get('end_node_name')
        floor = request.GET.get("floor","0")
    image_path = r'static\assets\image.jpg' if floor == "1" else r"static\assets\floor0.jpg" 
    node_coordinates = [(45, 233),      #A
                        (93, 195),      #B
                        (152, 188),     #C
                        (384, 184),     #D
                        (426, 133),     #E
                        (461, 190),     #F
                        (707, 197),     #G
                        (768, 222),     #H
                        (765, 280),     #I
                        (728, 317),     #J
                        (548, 326),     #K
                        (487, 304),     #L
                        (368, 305),     #M
                        (325, 305),     #W
                        (271, 318),     #O
                        (202, 359),     #P
                        (96, 350),      #Q
                        (66, 315),      #R
                        (171, 386),     #S
                        (618, 386),     #T
                        (141, 229),     #N1
                        (150, 325),     #N2
                        (97, 288),      #N3
                        (296, 244),     #N4
                        (383, 227),     #N5
                        (458, 245),     #N6
                        (515, 256),     #N7
                        (614, 255),     #N8
                        (684, 253),     #N9
                        (250, 284),     #N10
                        (618, 313),     #N11
                        (418, 242),     #N12
                        (193, 242)]     #N13  
    node_names = ['Laboratory', 'Reprographic center', 'Lab-205', 'Office', 'Ground-floorLift', 'System Administrator',
                'Project lab', 'Language lab', 'Class room', 'Stairs near PG lab', 'Conference room', 'Office',
                'Meeting room', 'Principal-Conference room', 'Principal office',
            'Reception', 'Drinking water', 'Stairs opp to documentation','Main Entrance','Entrance-2',
                'Near documentation','Near reception','Near stairs', 'Near to prinipal office','Near to turning',
                'Near to Turning','Near to conference room','Near to closed entrance','Near to Project lab',
                'Near principal room','Near to back door','Near to lift','Near laboratory']


# result if condition floor ==1 else  else_result

    node_info = {name: coordinates for name, coordinates in zip(node_names, node_coordinates) if name.startswith('N')}
    print(node_info)


    start_node_coordinates = None
    for i, name in enumerate(node_names):
        if name == start_node_name:
            start_node_coordinates = node_coordinates[i]
            break
    print(start_node_coordinates)        
   
    end_node_coordinates = None
    for i, name in enumerate(node_names):
        if name == end_node_name:
            end_node_coordinates = node_coordinates[i]
            break
   
    
    node_info[start_node_name] = start_node_coordinates
    node_info[end_node_name] = end_node_coordinates

    # node_info
    print(node_info)
    shortest_path_indices = find_shortest_path(node_info, str(start_node_name), str(end_node_name))
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)
    node_names_in_path = [node_names[idx] for idx in shortest_path_indices]


    img = insert_nodes(image_path, node_coordinates, node_names, start_node=start_node_name, end_node=end_node_name, path_nodes=node_names_in_path)

    img = draw_path(img, shortest_path_indices, node_coordinates)
    # Your existing code to find shortest path and generate directions
    
    # print(start_node_name)
    # print(end_node_name)


    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    image_filename = f'navigation_image_{start_node_name}_{end_node_name}.jpg'  # Unique filename
    image_path = os.path.join(r"static", 'navigation_images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Print directions
    direct = ", then, ".join(directions)+ ". Thank You! "
    print(direct)
    response_data = {
        "directions": direct,
        "image_filename": image_filename  # Include the image filename in the response
    }

    return render(request, "preview.html", response_data)









































