# In the Margins Content Guide


## <a name='overview'></a> Overview
* [Overview](#overview)
* [What is This?](#this)
* [Helpful Tips](#tip)
* [A General Introduction to In the Margins](#intro)
* [How to Embed Content in Lexos](#howto)

---


## <a name='this'></a> What is This?
* This is the development manual for Lexomics project staff producing content for In the Margins. It is especially aimed 
* at how to create content for use in Lexos.

---


## <a name='tip'></a> Helpful Tips
#### 1. The Scalar manual can be found at [http://scalar.usc.edu/works/guide/index](http://scalar.usc.edu/works/guide/index).
#### 2. Pay special attention to the unusual vocabulary used by Scalar.
#### 3. The url for *In the Margins* is [http://scalar.usc.edu/works/lexos](http://scalar.usc.edu/works/lexos). A full Scalar URL will end with a "slug" for each individual page (e.g. [http://scalar.usc.edu/works/lexos/best-practices](http://scalar.usc.edu/works/lexos/best-practices), where "best practices" is the slug). Make sure to give each node a coherent slug using hyphens to separate words.

---


## <a name='intro'></a> A General Introduction to In the Margins
* *In the Margins* is a multimedia "book" published on the [Scalar](http://scalar.usc.edu/) platform produced by the The Alliance for Networking Visual Culture at the University of Southern California (which hosts the content). The url for In the Margins is [http://scalar.usc.edu/works/lexos](http://scalar.usc.edu/works/lexos). This should probably be changed to [http://scalar.usc.edu/works/in-the-margins](http://scalar.usc.edu/works/in-the-margins). *In the Margins* also refers to re-usable content stored in the Scalar platform which can be accessed by Lexos through the [Scalar API](http://scalar.usc.edu/features/open-api/). Essentially, Lexos sends a message to Scalar asking it to send back specific content. This can be individual pages of *In the Margins* or media files such as videos. It can even be text snippets for use in the Lexos User Interface.

When producing content for *In the Margins*, it is important to remember this dual use. If content is to appear separately in the Scalar book and Lexos, it is better to produce an independent node for that content, which can be accessed by either a Scalar page or an element in Lexos. Be very aware of the titles you provide for this material. Generally, the title will be re-used automatically by Lexos, whereas the reader of the Scalar book will access the content by the title of page in which it is embedded.

The API works by sending a request for a particular Scalar url to Scalar, which returns a JSON object containing metadata and content for the requested url. The JSON object is parsed in `js/scripts_ITM.js`.

Currently, the Lexos `scripts_base.js` file begins with the following code:

```Javascript
  // Load the Scalar API and cache it.
  $.ajax({
    url: "scalarapi.js",
    dataType: "script",
    cache: true
  });
```

This loads the Scalar API script and commits it to the browser cache. It will therefore be available on any Lexos page without the need to reload it.

---


## <a name='howto'></a> How to Embed Content in Lexos

* Lexos currently has three methods of embedding *In the Margins* content: the side panel, a pop-up dialog, and a pop-up dialog containing a video. Other content "hooks" may be added in time.

### Using the Side Panel
By default, the side panel displays *In the Margins* content for the current screen. In other words, if you are on the Scrub screen, the panel will display the *In the Margins* Scrub page. The content is set by two methods:

1. In `lexos.py` the route's GET request must return `itm="SLUG"` where `SLUG` is the slug in the Scalar URL.
2. In the current configuration `base.html` contains the following code in the banner:

```html
<a href="{{url_for('base')}}" id="titlelink">
   <span id="titleprefix" data-slug="{{ itm }}">Lexos</span> &#123;{% block title %}{% endblock %}&#125;
</a>
```

The `data-slug` attribute contains the `itm` value (the slug), designated in `lexos.py`. If no slug is passed to the template, Lexos will automatically display the content at [http://scalar.usc.edu/works/lexos/index](http://scalar.usc.edu/works/lexos/index).

The default content may be overridden using elements in the Lexos UI. For instance, say you wanted a button to open the panel and display an *In the Margins* page containing the [Philosophers Song](http://www.metrolyrics.com/the-philosophers-song-lyrics-monty-python.html) from Monty Python. Your button would look like this:

```html
<button class="ITMtrigger panel" data-slug="philosophers-song">Some philosophy</button>
```

The class `ITMtrigger` identifies the button as a trigger for *In the Margins* content to be displayed, and the class `panel` indicates that the content should be displayed in the panel (which will open automatically). The `data-slug` attribute contains the slug of the page containing the content. Lexos will send an API request to Scalar for the specific content, parse the result, and place the content in the panel.

### Pop-up Dialogs:

Pop-up dialogs are JQuery UI dialogs containing *In the Margins* content, generally text. To trigger a pop-up dialog from a Lexos UI element, create a trigger like the following in the Lexos template file:

```html
<button class="ITMtrigger dialog" data-slug="philosophers-song">Some philosophy</button>
```

Lexos uses the title of the Scalar page for the JQuery UI dialog's title. Currently, this cannot be overridden.

### Video Dialogs:

Scalar can only store videos under 2MB in size. As a result, it is often practical to store videos on YouTube, Vimeo, or other services. Scalar pages can then access those videos through the services' APIs. Lexos, however, has to access them through the videos metadata stored in Scalar. Since the metadata is slightly different for each service, Lexos needs a different function for different types of videos. *Currently, Lexos can only handle YouTube videos.*

To create a video dialog, use a trigger element like the one below:

```html
<button class="ITMtrigger video-dialog" data-slug="philosophers-song-video">Watch the Video</button>
```

Lexos will send an API request for page containing the video metadata. If the result contains a recognised format, it will display the video in the pop-up dialog.

### How to Embed YouTube Videos:

This is a complicated process. When the video is uploaded to YouTube, it is assigned an ID number for embedding. You can find that at the end of the url, which will look something like `https://www.youtube.com/watch?v=l9SqQNgDrgg`.

Do not grab the YouTube embedding code and place it in a Scalar page. In Scalar, the video must have its own node so that it can be accessed independently of other content. The steps to do this are provided below:

1. Go to the Scalar Dashboard and click the **Media** tab.
2. At the top right of the screen, select **YouTube** from the **Import Pages dropdown**.
3. In the **Search** menu, enter the ID of the YouTube video (e.g. `l9SqQNgDrgg`). When the video appears, click **Import Selected**.
4. In the **Media** tab, click the link for the video and then click the **Edit** button at the bottom of the screen. Change the title as necessary. Make sure that the **Media url* is something like `https://www.youtube.com/watch?v=PYUtMbxXcUg`. This will load YouTube's default HTML5 video viewer. A url like `http://www.youtube.com/v/l9SqQNgDrgg` will load YouTube's Flash viewer, which may not work in some browsers.
5. Click the **Metadata** link at the bottom of the page. Notice the **Scalar url** section. The full url is `http://scalar.usc.edu/works/lexos/` plus the Scalar slug. You can only edit the slug. Change it to something that makes sense and remember the slug. You will use this in the `data-slug` attribute of the element that triggers the video dialog.

You have now created a media object, which can be requested by Lexos through the API. You can also embed the video in any Scalar page by clicking the Add inline Scalar media file button in the toolbar (scroll over the icons until you get a popup that tells you which one).

**Important: YouTube occasionally changes its API format, which will break the system. We need to keep an eye on changes so that we do not lose access to content.**