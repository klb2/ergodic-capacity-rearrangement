FROM rpy2/jupyter-ubuntu:master-20.04


ARG NB_USER=jupyteruser
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

# user jupyteruser already created in container
#RUN useradd -m --uid ${NB_UID} ${NB_USER}

#ENV R_LIBS_USER /home/${NB_USER}/R/packages

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
RUN usermod -a -G staff ${NB_USER}
USER ${NB_USER}

RUN pip3 --no-cache-dir install -r ${HOME}/requirements.txt
RUN R -e "install.packages('qrmtools',dependencies=TRUE)"
