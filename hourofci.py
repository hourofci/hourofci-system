import ipywidgets as widgets
import requests
# Retrieve username
import getpass

# Input:
# lesson (e.g., "geospatial-data")
# lesson_level (e.g., "beginner")
# question - defined behind instead of in the notebooks
# widget - the widget of which value will be submitted

def SubmitBtn(lesson,lesson_level,question,widget):
    # Submit button
    button = widgets.Button(
        description = 'Submit',
        disabled = False,
        button_style = '',
        icon = 'check'
    )
    
    display(button)
    
    # Output
    output = widgets.Output()
    display(output) 
    

    # Submit function
    def submit(b):

        # Logging
        host = "check.hourofci.org"
        port = "4000" 
        answer = widget.value
        # v6 - Retrieve username
        username = str(getpass.getuser())
        # v6 - Add username
        url = "http://{}:{}/{}/{}/{}/{}/{}".format(host, port, username, lesson, lesson_level, question, answer)
        # print(url)
        # Send_request
        r = requests.get(url)

        # Print widget value
        with output:
            output.clear_output()
            print(widget.value)
            if r.status_code == requests.codes.ok:
                print("Submit Successfully!")
    
    button.on_click(submit)