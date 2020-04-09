# Installation and Configuration of Hour of CI JupyterHub

## 1. Prerequisites

You need a Jetstream account with an XSEDE allocation.

## 2. Installing the littlest JupyterHub on JetStream 

Step 1. Log into [the Jetstream portal](https://use.jetstream-cloud.org/).     

Step 2. Select the **Ubuntu 18.04 Devel and Docker** image and launch.  

Step 3. In the dialog **Launch an Instance / Basic Options**, type your own **Instance Name** and select **m1.medium** (recommended) under **Instance Size**.

Step 4. Click **Advanced Options**, and then click **Create New Script**. 

In the new dialog box,
* under **Input Type**, select **Raw Text**;  
* under **Execution Strategy Type**, select **Run script on first boot**;  
* under **Deployment Type**, select **Wait for script to complete**.  

Copy the text below, and paste it into the **Raw Text** text box. Replace `<admin-user-name>` with the name of the first admin user for this JupyterHub.   
```bash
#!/bin/bash
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
  | sudo python3 - \
    --admin <admin-user-name>
```

After that, Click **Save and Add Script** and then click **Continue to Launch** to finish configuring the advanced options.  

Step 5. Click **Launch Instance**, and your server is getting created. You can see the status on the dashboard.  When the status is Active and the progress bar become a solid green, your JupyterHub is ready for use.

Step 6. Copy the IP Address of your server and access it from a web browser. You will go to the JupyterHub login page. Use the admin username set in the deployment script, and set a password when first log in.  

Now, you can work with your JupyterHub.   

![jupyterhub](images/jupyterhub.png)

See more details on [Installing of the Littlest JupyterHub](https://tljh.jupyter.org/en/latest/install/jetstream.html).

## 3. Installing Packages for All Users

The packages/ extensions required in Hour of CI include:
* [RISE](https://rise.readthedocs.io/en/maint-5.6/installation.html): turn jupyter notebooks into a live presentation;
* [jupyter_contrib_nbextensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions): contains a collection of extensions that add functionality to the Jupyter notebook

Installing packages in the terminal of JupyterHub may do not work. Thus, we install packages outside JupyterHub. 

Step 1. Go to the project page on [the Jetstream portal](https://use.jetstream-cloud.org/), and click **Open Web Shell**

Step 2. Since we are outside JupyterHub, we need to change PATH to access user environment outside first
```shell
export PATH=/opt/tljh/user/bin:${PATH}
```

Step 3. Install
```shell
sudo env PATH=${PATH} conda install -c conda-forge jupyter_contrib_nbextensions

sudo env PATH=${PATH} conda install -c conda-forge rise
```

Similar way to install other packages. For example,
```
sudo env PATH=${PATH} conda install -c conda-forge gdal
```

Note: When using sudo, the PATH environment variable is usually reset, for security reasons. Thus, we nned to specify the PATH

Step 4. Enable extensions
After installing contributed extensions, you can enable the extensions you would like to use. The syntax for this is jupyter nbextension enable followed by the path to the desired extension’s main file. In Hour of CI, two extesions will be enabled: `init_cell` and `python-markdown`:
```shell
sudo env PATH=${PATH} jupyter nbextension enable init_cell/main --sys-prefix

sudo env PATH=${PATH} jupyter nbextension enable python-markdown/main --sys-prefix
```

You can see the enabled extensions in the list: 
```shell
jupyter nbextension list
```

Note: Don't use the Nbextensions tab (jupyter_nbextensions_configurator) to enable or configure the extensions. The changes using the Nbextensions tab will only apply to your account instead of user environments. In addition, a nbconfig directory will be created in your home folder and overwrite the file in the system


## 4. Other Configurations
You can use tljh-config to configure the Littlest JupyterHub.   

In Hour of CI, we try to shutdown the server after no activity for 20 minutes:
```shell
sudo tljh-config set NotebookApp.shutdown_no_activity_timeout 1200
```

After modifying the configuration, you need to reload JupyterHub for it to take effect:
```shell
sudo tljh-config reload
```

You can go to [Configuring TLJH using tljh-config](http://tljh.jupyter.org/en/latest/topic/tljh-config.html#reloading-jupyterhub-to-apply-configuration) and see how to set other properties.


## 5. Adding Users
In the default authentication method, admin users can [add users in the admin page](https://tljh.jupyter.org/en/latest/install/jetstream.html#step-2-adding-more-users), and users use the assigned username choose a password when they first log in.   

## 6. Sharing Data

nbgitpuller is a Jupyter Notebook extension that helps distribute study materials / lab notebooks to students. Users of your JupyterHub can **click a nbgitpuller link** to fetch the latest version of materials from a git repo.

You can use an [application for nbgitpuller link generation](https://mybinder.org/v2/gh/jupyterhub/nbgitpuller/master?urlpath=apps/binder%2Flink_generator.ipynb).

See more details on [Distributing materials to users with nbgitpuller](https://tljh.jupyter.org/en/latest/howto/content/nbgitpuller.html).

Here is a link for a Hour of CI notebook demo: https://pilot.hourofci.org/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2FIrisZhiweiYan%2Fhourofci-demo&subPath=geospatial-data%2Fgd-1.ipynb&app=notebook