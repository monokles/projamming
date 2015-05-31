==projamming==

Create music using network packets as a source for audio. Ever wondered what DHCP sounds like?

Our project turns packets that go over the network into sound. It creates a piece of ambient music from the standard network traffic, but you can also create rhythms by pinging the server. You can contribute to the sound by manually sending bytes to it, or even write a script to make a beat.

It allows you to "jam" with multiple computers by connecting to the server and sending whatever you want to it. Different computers produce different sounds. Even just connecting to the network already generates traffic, which translates into sounds.

===The technology===

We used python with pygame for playing sound. We listen on the network directly without a library using a raw socket. We also used some samples from Sonic Pi. And a lot of Club Mate to stay awake.
