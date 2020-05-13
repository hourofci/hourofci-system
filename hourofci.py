import ipywidgets as widgets
import requests
# Retrieve username
import getpass
# Encoding
import hashlib

# Input:
# lesson (e.g., "geospatial-data")
# lesson_level (e.g., "beginner")
# question - defined behind instead of in the notebooks
# widget - the widget of which value will be submitted

# v7 - Add user_agent parameter, which is from the notebook
def SubmitBtn(user_agent,lesson,lesson_level,question,widget):
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
        # username = str(getpass.getuser())
        username = str(getpass.getuser()).split('-')[1] # In Jupyterhub, getuser() = Jupyter-username
        # v7 - Encode username
        username_hash = hashlib.md5(username.encode()).hexdigest()

        # v7 - Encode user agent
        user_agent_hash = hashlib.md5(user_agent.encode()).hexdigest()

        # v6 - Add username 
        # v7 - Add user agent
        url = "https://{}:{}/{}/{}/{}/{}/{}/{}".format(host, port, username_hash, user_agent_hash, lesson, lesson_level, question, answer)
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