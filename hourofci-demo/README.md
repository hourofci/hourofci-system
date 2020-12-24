# Set Up a Hour of CI Lesson

## File Organization
The organization of our lessons and the supplementary files are in hourofci-demo.
hourofci.py and JavaScript files are under the supplementary folder.
The path of a lesson notebook should be \<lesson-level>\<lesson>\<filename>.ipynb
The relevant files (e.g., HTML files, images) are in  \<lesson-level>\<lesson>\supplementary   

<br>

## Template notebook
We provide a template for the lesson notebook, which is in \template-lessons\template\template.ipynb

When you go back to the normal jupyter notebook, you can find a toggle button for raw code. When you click this button, all the code cells that are hidden in this notebook will be shown. The cell for the button should be in every lesson notebook. It starts the following setup for a Hour of CI lesson notebook:
Import Python libraries
* Import hourofci.py
* Load custom.js 
* Hide output indicator (e.g., Out[1])
* Hide code by introducing a toggle button "Toggle raw code"  

This cell is set to be:
* An initialization cell (Toolbar > View > Cell Toolbar > Initialization Cell is checked)
* A cell that is not displayed in slide (the Slide Type is 'Skip')

In the following cells, there are many examples showing how to use the notebook (our notebook has some custom settings because hourofci.py and custom.js are loaded).
* Initialize or hide a code cell by adding tags “Init” or “Hide” (defined in custom.js)
* Insert a HTML file using IFrame.
* Record the action “a user does run the code” by adding a tag (The play button is defined in custom.js).
* Insert an image
* Create a widget (any type of widget) and a submit button which can submit the answer to our database (The submit button is defined in hourofci.py).  

<br>

## Custom.js
This file customizes Hour of CI lesson notebooks:
Get the user agent string, lesson and lesson level from the webpage url automatically.
Pass them to Python variables, so we can use them in the notebooks.
Configure or run a code cell based on their tags 
`Init`: automatically run the code cell when users’ open the notebook
`Hide`: hide the raw code and only display the output
question format `[1-9][A-Z]`: usually used for the code which users are asked to learn and run. If a code cell has this kind of tag, “Run” will be recorded if the user clicks the play button of the code cell.
Record if users click a link (e.g., “Go to the next section”) by adding a class `link-logging`.

<br>

## Hourofci.py
The main part in this file is the `SubmitBtn` function. Notice that two different APIs are used for production and for testing purposes.

<br>

## HTML files
In addition to widgets, there is another group of interactions created by HTML. We can modify a normal HTML to log the interactions.

Step 1. Load Scripts, including D3, jQuery, jQuery md5 plugin, and other JavaScript files related to this HTML.

```html
<head>
  ...
  <!-- load D3 -->
  <script src="https://rawcdn.githack.com/coopbri/hci-binder/362464110b5273593e9fdd1dc1c0ae3e4f1da224/lib/d3.min.js"></script>
    
  <!-- logging: load jQuery (bundled with Jupyter; only needed outside of Jupyter) -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

  <!-- logging: load jQuery md5 plugin -->
  <script src="https://rawcdn.githack.com/placemarker/jQuery-MD5/b985fce4e867773e5fb7a29b4fb5df74c53595d0/jquery.md5.js"></script>
  ...
</head>
```

Step 2. Get the variables for logging

```html
<script>  
  var user_agent_hash = $.md5(navigator.userAgent);
  var answer;
  var url_pre = "https://check.hourofci.org:4000/"+user_agent_hash+"/<lesson>/<level>/<question>/";
  ...
</script>  
```

Here `<lesson>/<level>/<question>` is specific for a file. For example, if the interaction is the first question in gd-1.ipynb (geospatial-data) in the beginner-lessons folder, url_pre should be 
var url_pre = "https://check.hourofci.org:4000/"+user_agent_hash+"/geospatial -data/beginner/1A/";

Step 3. Send an API request when an action is taken (e.g., click a button, move an object). Here is an example where “true” will be recorded when the correct answer is clicked.

```html
<script> 
  var correct = d3.selectAll(".correct").on("click", function() {
	  ...
    // logging: log "True" when click the correct space
    answer = true;
    url = url_pre+answer;
    $.ajax({
      type: 'GET',
      url: url,
      success: function() {
        console.log("Answer is true");
      },
      error: function() {
        alert("Error");
      }
    });
  });
...
</script>
```

AJAX is used to output messages, helping developers to check whether the request is sent successfully or not. If you do not need any message, simpler code can be used to replace : `$.ajax()`:

```javascript
  answer = true;
  url = url_pre+answer;
  $.get(url);
```

Step 4. File path problem

All file paths in HTML and JavaScript files need to be hard-coded. Relative paths do not work. One solution is uploading the resources to GitHub first and then generating URLs using https://raw.githack.com/ 
