# Fiji - Arnheim

### Disclaimer

This is alpha software. Versioning is errounous. Breaking changes happening on a daily basis. If you want to test the Arnheim platform please contact the developers directly.

### Idea

Fiji-Arnheim provides a simple interface to start Fiji and connect it to a local Arnheim Instance. Fiji register itself
as a worker and provides implementations to common image analysis tasks. ImageJ-1 Macros are supported to wrap and are registered
as templates for the Tasks. (For detailed information on how Arnheim thinks about tasks and templates please visit the Arnheim
documentation)

 
### Prerequisites and Install

Fiji Arnheim heavily relies on PyImageJ for interfacing with ImageJ/Fiji. PyImageJ itself has various dependencies on Java and Maven.
You can install PyImageJ via conda and then install Fiji Arnheim on top.

```
conda create -n fijiarnheim pyimagej openjdk=8
conda activate fijiarnheim
pip install fiji-arnheim

```

This install pyimagej together with maven. PyImageJ is then taking care of setting up a local instance of Fiji.


### Usage

In order to run fiji-arnheim, activate your environment and run
```
fiji-arnheim
```
This will open Fiji with its UI (Usage is standard Fiji) and register it as a worker. You can call its implementations
now from anywhere


### Use Cases

Please read the Arnheim documentation thoroughly to get an idea for the use-cases and limitations of the Arnheim platform.
Use cases include:

  1. Remote Image Analysis: Use data stored on your institute server and analyse it on your local machine, without downloading and storing your data.
  2. Big Data: Stream big datasets to your local machine (Napari required)
  3. Combined Analysis Flows: Use Deeplearning in the Cloud, Cluster analysis, Web apps and Clients like ImageJ and Napari all in one analysis flow with metadata storage.
  4. End-to-End Pipelines: Acquire Images on your Microscope, process them on the fly and get notified about results.

Please contact the developer for better explainations.


### Testing and Documentation

So far Arnheim Fiji does only provide limitedunit-tests and is in desperate need of documentation,
please beware that you are using an Alpha-Version


### Build with

- [Arnheim](https://github.com/jhnnsrs/arnheim)
- [Bergen](https://github.com/jhnnsrs/bergen)
- [Grunnlag](https://github.com/jhnnsrs/grunnlag)
- [PyImage](https://github.com/imagej/pyimagej)



## Roadmap

This is considered pre-Alpha so pretty much everything is still on the roadmap


## Deployment

Contact the Developer before you plan to deploy this App, it is NOT ready for public release

## Versioning

There is not yet a working versioning profile in place, consider non-stable for every release 

## Authors

* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) 

## Acknowledgments

* EVERY single open-source project this library used (the list is too extensive so far)