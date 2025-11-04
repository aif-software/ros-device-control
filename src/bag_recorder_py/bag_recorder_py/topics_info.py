from sensor_msgs.msg import PointCloud2, Image

info = [
    # Lidar
    {
        "name": "/lidar_points",
        "type": PointCloud2,
        "typestring": "sensor_msgs/msg/PointCloud2",
    },
    # Flir
    {
        "name": "/image_raw",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    # Stereo camera
    {
        "name": "/aux/image_color",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    {
        "name": "/left/cost",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    {
        "name": "/left/depth",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    {
        "name": "/left/image_rect",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    {
        "name": "/right/image_rect",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
]
