import React, { useRef, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import * as maptilersdk from '@maptiler/sdk';
import "@maptiler/sdk/dist/maptiler-sdk.css";
import './App.css'; 
import './map.css';
import logo from './logo-1.png';

const maptilerApiKey = "OjEUDMaMdUwGomWdF0NV"; 
const googleMapsApiKey = "AIzaSyA3g32S0rG5NcfPKC4QzJyvadFA73JpYl0"; 

const place = "Marston Quad Pomona College"

function MapPage() {

  const mapContainer = useRef(null);
  const map = useRef(null);
  const claremont = { lng: -117.71350614401385, lat: 34.09932899451676 };
  const [zoom] = useState(15);
  maptilersdk.config.apiKey = maptilerApiKey;

  useEffect(() => {
    if (map.current) return; // stops map from intializing more than once

    map.current = new maptilersdk.Map({
      container: mapContainer.current,
      style: maptilersdk.MapStyle.STREETS,
      center: [claremont.lng, claremont.lat],
      zoom: zoom
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
