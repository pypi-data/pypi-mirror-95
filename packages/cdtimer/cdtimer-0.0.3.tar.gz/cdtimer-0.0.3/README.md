# Countdown timer

A countdown timer with large display that counts down from a set time or goes through sequenced intervals. Optionally plays sound at given interval frequency or loads timetable of tasks.

### Usage
- **Countdown time**: Enter in top left window for total countdown time.
- **Interval sound frequency** (optional, top right window): For sound signal in given frequency. 
- **Timetable** (optional, Browse files): Choose timetable to enable guided countdown. 
- **Timetable format**: See example file in <code>./timetables/</code>. Enter comma seperated:
  - Task
  - Repetition number per set-any extra information to display
  - Set number per task
  - Time per set
  - Order of sets
- **Sound**: Turn sound effects on/off at the bottom. 
- **Time format**: Any given HH:MM:SS, MM:SS, SS format. 
- **Start**: Use the Start/Stop button to start the countdown.
- **Next** (only for loaded timetables): Skip to next set

### Dependencies
- Tkinter (<code>apt-get install python3-tk</code>)
- [SoX - Sound eXchange](http://sox.sourceforge.net/) - Only if you want to play sound. 
Install for Linux (<code>apt-get install sox</code>) or via PyPi (<code>pip install sox</code>).

### Credits 
Daniel Vogler



![Example image](/images/countdown_example.png "Example of countdown")

![Example image timetable](/images/countdown_example_timetable.png "Example of timetable use")

