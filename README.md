# Signal-generator-and-Sampler
generate desired sinsoudal and sample it with desired frequency

We created a GUI using tkinter python that illustrates the Nyquist-Shannon sampling theorem\
The application supports the following options:\
1.Compose a signal by adding sinusoidals with specified magnitude,frequency and phase shift\
2.Sample the signal with adjustable sample rate\
3.Reconstruct the sampled points using sinc reconstruction method\
4.Import a nonsynthetic signal from an excel sheet (csv) to test the sampling and reconstruction on more complex signals
The following video shows most of the application functionalities:


https://user-images.githubusercontent.com/101192969/157289816-901ad2f5-556b-4499-95d6-9388ffb408c2.mp4




The following screenshots shows sampling a real ECG signal imported from CSV file:

Undersampled:

![image](https://user-images.githubusercontent.com/101192969/157290341-bb84bc39-2915-4fa4-b15d-29a25335f823.png)


Oversampled:

![447af95c-0363-489b-8f97-68e46e8906a6](https://user-images.githubusercontent.com/101192969/157290222-b58b8df2-dbd8-42a6-94d0-906c5c2689af.png)
