Overview
======================
This project is a Flask-based web application built to manage and visualize [Vonage Opentok Experience Composer (EC)](https://tokbox.com/developer/guides/experience-composer/) sessions. It provides a browser-based dashboard to create sessions and tokens, start/stop Experience Composer, Archiving, and Boradcasts, all controlled via OpenTok Python SDK. On the client side, it uses the OpenTok JavaScript SDK to publish and subscribe to streams, designed specifically for Experience Composer layout preview purposes.

How It Works
======================
This project consists of 2 main scripts: `manage.py` and `view.py`.  

- `manage.py` is used to control the Experience Composer. It provides an interface to create sessions and tokens, start or stop the Experience Composer, and manage Archiving and Broadcasting.  
- `view.py` launches a web application intended to be used as the Experience Composer URL. The `/publish` endpoint initializes a publisher and displays it alongside a sample iframe of Google Map location. The `/subscribe` endpoint provides a subscriber-only view for Experience Composer rendering.  

Each script can be used independently. Use `manage.py` alone when testing with external, non-Video API URLs (e.g. https://www.unit9.com/ or https://inanimatealice.com/). Use `view.py` along with `manage.py` when testing with a real-world video app for publishing and subscribing. 

How to Use
======================
1. Initial Setup Ref: https://developer.vonage.com/en/video/server-sdks/python
```
$ python3 -m venv venv  
$ source venv/bin/activate  
(venv) $ pip install -r requirements.txt
```
2. Rename `.env-example` to `.env` and set the following variables:
```
VIDEO_PROJECT_API_KEY=          # Used by manage.py for server-side EC operations
VIDEO_PROJECT_API_SECRET=       # Same as above
VIDEO_SESSION_ID=               # Used by view.py for a web app where the actual publisher participates.
VIDEO_TOKEN=                    # Same as above
```

3. Start the Publisher/Subscriber Web App  
```
$ python3 view.py
```

4. This will automatically open `http://localhost:8080/subscribe`.  
In a new browser tab, open `http://localhost:8080/publish` to publish your camera stream.  
You should see that it is being subscribed on the `http://localhost:8080/subscribe` page.  
![Screenshot 2025-06-20 at 1 30 58 pm](https://github.com/user-attachments/assets/2af196a2-3260-42ae-838c-9b30721fee40)



5. To make the app accessible to be captured by Experience Composer:  
```
$ ngrok http 8080
```

6. Copy the public URL and update your `.env`:  
```
VIDEO_EXPERIENCE_COMPOSER_URL="https://<your-ngrok-url>/subscribe"
```

7. Now that your EC target is ready, launch the management interface:  
```
$ python3 manage.py
```

8. This opens `http://localhost:5000/manage`.  
1-First, click Create Session & Token.  
2-Then start the Experience Composer.  
3-Optionally, you can start Archive or Broadcast as needed.
![Screenshot 2025-06-20 at 1 24 17 pm](https://github.com/user-attachments/assets/79cb6782-16f7-4392-8813-5883dbd28ec1)




9. Customize Options (Optional)  
To change archive or broadcast options, edit `manage.py`. By default, HLS broadcasting is enabled. If you'd like to broadcast to YouTube or other RTMP targets, use [the uncomment sections in start_broadcast()](https://github.com/ydumburs/opentok-experience-composer/blob/main/manage.py#L123).  
