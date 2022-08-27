# The Safe Driver Coaching System

Strangely enough dangerous driving such as speeding and hard breaking is NOT the main cause of accidents.
Of all car accidents 94 percent are caused by driver error and 57 percent by distracted driving.

**``Note: The number of deadly and serious accidents is not decreasing for many years so we need to do something more radical.``**

The idea is change driver behavior by monitoring and improve driving style in order to reduce injuries and damages.

The driver coach system will check for all safety aspects (360 degrees 3D aspects):

* Warn for [Distractions]
* Alert for [Drowsiness]
* Improve your [Driving style and skills]

In this approach is the idea of providing each driver with an AI based personal driving coach. The driving coach combines the knowledge of a group of expert driving coaches, assesses your driving and provides valuable feedback to make driving safer. As far as i know there is currently no system that monitors the driver while executing vehicle maneuvers.

**The objective is to make driving safer by developing an affordable personal driving coach. Therefore I open sourced this plan and its code and hope others including companies and organisations will step in and adopt it.**


Approach:
* Get more people involved in the project (developers, safety experts, evangelists, test dummies)
* Verify that the idea is sound and can result in an affordable and fully functioning solution
* Develop a working demonstration to show its capabilities
* Develop software components and building blocks (software libraries, hardware design, system configurations)
* Open source the idea, plans, methods and software libraries
* Broadcast the idea, get organisations involved
* Deliver a device that can do the job and is afforable for everyone

## The business case
We get the best for everyone by help of the Companies that care about social responsibility to their customers should consider all previous arguments and 
design a system that provides real benefits for their customers.
Such a system is however more complex and costly to develop and implement. An open source solution might be helpful to reduce cost if its flexible enough to be adapted to specific requirements.

**So the main question is: How can we develop an affordable and flexible solution that provides benefits for all**

|Consumer|Business case|
|----------|-----------|
|* Promote safe driving habits|* Car lease (safety as a service, reduce car accidents)
| * Improve safe driving behaviour|* Insurance (reduce car accidents)
| * Help to prevent car accidents|* Road service organizations (safety for its members)
| * Make Driver Monitoring systems available for low cost|* Driving school (better feedback, better results)
| * Lower costs for society|
| * While keeping privacy|

A good starting point to introduce this system would be driving schools.
They could use these devices in their daily practice and lend them to their customers when they practice under parental supervision. 
By lending them to young drivers on training, consumers will getting used to these devices and this will lead to general acceptance.

# How to develop and implement

## How the system works
When a driver enters the car he/she is automatically recognized with face recognition.
During the trip the system continuously determines the actual driving situation (parked, cruising, braking, turning) and evaluates the drivers activity and behaviour.
It provides an audible warning when the driver gets tired and requires a break.
It immediately alerts the driver when a dangerous situation occurs, such as changing direction without signaling or texting while driving. 

After each trip the system sends a summary to the driver's smartphone for quick review. 
When at home specific situations can be reviewed in depth with the Driving Coach App. 
The App will show snapshots or short video with detailed data and advise for improvement.

The collected data is kept on the device under full control of the driver and can be deleted when required.
Data can be shared with selected parties for specific applications such as an insurance company or a safe driver leader board  where drivers can compare themselves with other drivers.

## Monitoring driver behavior

  * Good driving habits
    * Wearing seat belt
    * Active driving posture
    * Hands on the steering wheel
    * Looking to the general driving direction
    * Checking for traffic from all directions
    * Left/right/rear mirror checking
    * Signalling direction changes to other drivers
   * Abstain from distractions
     * Mobile phone usage (handheld, call, texting)
     * Operating the console (radio / airco)
     * Talking to passengers
     * Eating or drinking
     * Other (reaching for something, singing)
   * Driver physic
 
 
## Tools and technology
 
 * Driver Sensors     
    * Face location (is there a driver)
    * Driver recognition (who is driving)
    * Head Pose estimation (looking direction)
    * Face landmarks (eyes, mouth)
    * Hand location (on steering wheel)
    * Image classification of dangerous situations
 * Vehicle sensors
    * Acceleration (left/right turn, breaking)
    * Vehicle speed
 * Tools
    * Python, OpenCV (CV2), Dlib, fast.ai
    * Python-video-annotator 
    * UAH DriveSet Reader
 * Datasets
    * StateFarm Distracted Driver dataset 
    * Eyeblink8 
    * Columbia Gaze DataSet 
    * DMD - Driving Monitoring Dataset 
 * Example solutions
   * Futurebridge 
 * Example code:
    * Learn Open CV Examples
    * Brain4Cars technical research 
    * Ground AI Real-Time Driver State Monitoring
                Using a CNN Based Spatio-Temporal Approach*

