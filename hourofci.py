import ipywidgets as widgets
import requests

# Input:
# lesson (e.g., geospatial-data)
# lesson_level (e.g., beginner)
# question - ???which type
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
        # print widget value
        with output:
            output.clear_output()
            print(widget.value)

        # logging
        host = "check.hourofci.org"
        port = "4000" 
        answer = widget.value
        # http://127.0.0.1:5011/<lesson>/<lesson_level>/<question>/<answer>
        url = "http://{}:{}/{}/{}/{}/{}".format(host, port, lesson, lesson_level, question, answer)
        # print(url)
        # send_request
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            print("Submit Successfully!")
    
    button.on_click(submit)