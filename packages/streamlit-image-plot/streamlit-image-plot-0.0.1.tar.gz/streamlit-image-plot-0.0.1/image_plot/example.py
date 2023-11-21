import streamlit as st
from __init__ import image_plot

data= [
    {
      "id": 0,
      "title": "Attack Speed",
      "data": [
        {
          "id": 0,
          "label": "equipment 1",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/f/f3/Corrosion_Scythe.png",
          "width": "100%"
        },
        {
          "id": 1,
          "label": "equipment 2",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/1/1a/Demon_Hunter_Sword.png",
          "width": "100%"
        },
        {
          "id": 2,
          "label": "equipment 3",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/e/ed/Feather_of_Heaven.png",
          "width": "100%"
        },
        {
          "id": 3,
          "label": "equipment 4",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/e/e0/Active_-_Conceal.png",
          "width": "100%"
        }
      ]
    },
    {
      "id": 0,
      "title": "Attack Speed",
      "data": [
        {
          "id": 0,
          "label": "equipment 1",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/f/f3/Corrosion_Scythe.png",
          "width": "23%"
        },
        {
          "id": 1,
          "label": "equipment 2",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/1/1a/Demon_Hunter_Sword.png",
          "width": "13%"
        },
        {
          "id": 2,
          "label": "equipment 3",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/e/ed/Feather_of_Heaven.png",
          "width": "53%"
        },
        {
          "id": 3,
          "label": "equipment 4",
          "link":
            "https://static.wikia.nocookie.net/mobile-legends/images/e/e0/Active_-_Conceal.png",
          "width": "63%"
        }
      ]
    }
  ];

num_clicks = image_plot(data=data, key="foo")

