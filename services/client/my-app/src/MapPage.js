import React, { useRef, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import * as maptilersdk from '@maptiler/sdk';
import "@maptiler/sdk/dist/maptiler-sdk.css";

import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

import './App.css'; 
import './map.css';
import logo from './logo-1.png';

import axios from "axios";

const maptilerApiKey = "OjEUDMaMdUwGomWdF0NV"; 

const googleMapsApiKey = "AIzaSyA3g32S0rG5NcfPKC4QzJyvadFA73JpYl0"; 

function MapPage() {

  const mapContainer = useRef(null);
  const map = useRef(null);
  const claremont = { lng: -117.71350614401385, lat: 34.09932899451676 };
  const [zoom] = useState(15);
  maptilersdk.config.apiKey = maptilerApiKey;


  
  useEffect(() => {
    if (map.current) return; // stops map from intializing more than once
    
    axios
      .get("http://localhost:5001/all_events")
      .then((response) => {
        //handle successful response
        const markerData = response.data.map((eventInfo) => ({
          type: "Feature",
          properties: {
            id: eventInfo.id,
            name: eventInfo.name,
            description: eventInfo.description
          },
          geometry: {
            type: "Point",
            coordinates: eventInfo.location //need to use google maps geocoding api first
          },
        }));

        const mapInstance = new maplibregl.Map({
          container: mapContainer.current,
          style: 'https://api.maptiler.com/maps/bright/style.json?key=OjEUDMaMdUwGomWdF0NV',
          center: [claremont.lng, claremont.lat],
          zoom: zoom,
        });

        mapInstance.on("load", () => {
          console.log("Map loaded successfully");
        })

        map.current = mapInstance;
      })
      .catch((error) => {
        // Handle fetch error
        console.error("Error fetching events:", error);
      });
    
  }, [claremont.lng, claremont.lat, zoom]);

  return (
    <div className="App">
      <div className="top-bar">
        <h1>Map</h1>
      </div>
      <div className="left-bar">
      <img src={logo} alt="Logo" id="logo1" /> {/* Include the logo */}
        <ul>
        <li><Link to="/events">Events</Link></li>
        <li><Link to="/map">Map</Link></li>
        <li><Link to="/about">About</Link></li>
        </ul>
      </div>
      <header className="content">
        <h2>Map Page</h2>
        <div className="map-wrap">
          <div ref={mapContainer} className="map" />
        </div>
      </header>
    </div>
  );
}

export default MapPage;
