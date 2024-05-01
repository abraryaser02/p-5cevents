import * as maptilersdk from '@maptiler/sdk';
import "@maptiler/sdk/dist/maptiler-sdk.css";
import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import './App.css';
import ProfileIcon from './ProfileIcon';
import logo from './logo-1.png';
import './map.css';
import profileimg from './profileimg.png';

import axios from "axios";
import {
  fromAddress,
  setDefaults
} from "react-geocode";

const maptilerApiKey = "OjEUDMaMdUwGomWdF0NV"; 

const googleMapsApiKey = "AIzaSyA3g32S0rG5NcfPKC4QzJyvadFA73JpYl0"; 

const imageUrl = profileimg;

function MapPage() {

  const mapContainer = useRef(null);
  const map = useRef(null);
  const claremont = { lng: -117.71350614401385, lat: 34.09932899451676 };
  const [zoom] = useState(15);
  maptilersdk.config.apiKey = maptilerApiKey;

  // Set default response language and region (optional).
  // This sets default values for language and region for geocoding requests.
  setDefaults({
    key: googleMapsApiKey, // Your API key here.
    language: "en", // Default language for responses.
    region: "es", // Default region for responses.
  });

  useEffect(() => {
    if (map.current) return; // stops map from intializing more than once
    
    axios
      .get("http://localhost:5001/all_events")
      .then(async (response) => {

        //console.log("Events received from server:", response.data);
        //handle successful response
        const markerData = await Promise.all(response.data.map(async (eventInfo) => {
          try {
            const { results } = await fromAddress(eventInfo.location + " " + "Claremont")
            const { lat, lng } = results[0].geometry.location;
            //eventInfo.coordinates = [lng, lat]; // Assigning coordinates to eventInfo
            //console.log(eventInfo.location, [lng, lat])
            return {
              type: "Feature",
              properties: {
                id: eventInfo.id,
                name: eventInfo.name,
                description: eventInfo.description,
                location: eventInfo.location,
                organization: eventInfo.organization,
                start_time: eventInfo.start_time,
                end_time: eventInfo.end_time,
                contact_information: eventInfo.contact_information,
                registration_link: eventInfo.registration_link
              },
              geometry: {
                type: "Point",
                coordinates: [lng, lat]
              },
            };
          } catch (error) {
            console.error("Couldn't geocode event:", eventInfo.name);
            return {
              type: "Feature",
              properties: {
                id: eventInfo.id,
                name: eventInfo.name,
                description: eventInfo.description,
                location: eventInfo.location,
                organization: eventInfo.organization,
                start_time: eventInfo.start_time,
                end_time: eventInfo.end_time,
                contact_information: eventInfo.contact_information,
                registration_link: eventInfo.registration_link
              },
              geometry: {
                type: "Point",
                coordinates: [null, null] // Null coordinates
              },
            };
          }
        }));

        const mapInstance = new maptilersdk.Map({
          container: mapContainer.current,
          style: maptilersdk.MapStyle.STREETS,
          center: [claremont.lng, claremont.lat],
          zoom: zoom,
        });

        mapInstance.on("load", () => {
          console.log("Map loaded successfully");
        })

        mapInstance.on("load", () => {
          markerData.forEach((marker) => {
            const popupContent = `
            <h3>${marker.properties.name}</h3>
            <p><strong>Description:</strong> ${marker.properties.description}</p>
            <p><strong>Location:</strong> ${marker.properties.location}</p>
            <p><strong>Organization:</strong> ${marker.properties.organization}</p>
            <p><strong>Start Time:</strong> ${marker.properties.start_time}</p>
            <p><strong>End Time:</strong> ${marker.properties.end_time}</p>
            <p><strong>Contact Information:</strong> ${marker.properties.contact_information}</p>
            <p><a href="${marker.properties.registration_link}" target="_blank">Registration Link</a></p>
          `;

            const popup = new maptilersdk.Popup({ offset: 25 })
            .setHTML(popupContent);

            new maptilersdk.Marker({
              color: "#FF0000",
            })
            .setLngLat(marker.geometry.coordinates)
            .setPopup(popup)
            .addTo(mapInstance);
          });
        });

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
        {/* Profile icon */}
      <ProfileIcon imageUrl={imageUrl} />
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
