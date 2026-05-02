<script src="form.js"></script>
<style>@import url("//readme.codeadam.ca/readme.css");</style>

![LYSTEX Logo](images/lystex-logo-low.png)

<!--
<div style="position: relative; width: 100%; max-width: 100%; height: 0; padding-bottom: 56.25%; margin-bottom: 20px;">
    <video style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" controls poster="images/poster.png">>
        <source src="videos/demo.mp4" type="video/mp4">
    </video>
</div>

> <small>Music by: https://www.bensound.com/fre    e-music-for-videos License code: 38VOT6UMWYZVD3FW Artist: : Yunior Arronte</small>

---
-->

## What is LYSTEX?

[![LYSTEX](images/lystex-low.png)](images/lystex-high.png)

[LYSTEX](https://lystex.codeadam.ca) is a playable video game made entirely out of LEGO® bricks. Players use an Xbox controller to navigate a space rover through a series of puzzles to the bunker before the planet explodes.

### Game Stack

The playable game environment is built using LEGO® bricks. The interactive elements use LEGO® Spike™ and Pybricks (a custom firmware for the LEGO® Spike™).

[![LYSTEX Map](images/map-low.png)](images/map-high.png)

The LYSTEX Player App ia a companion application delivering video hints to the player as checkpoitns are completed. This app is building using vanillia HTML and JavaScript, [Firebase](https://firebase.google.com/), and [GitHub Pages](https://pages.github.com/). 

[![LYSTEX Control App](images/app-control.png)](https://lystex.codeadam.ca/player/control.html) [![LYSTEX Player App](images/app-player.png)](https://lystex.codeadam.ca/player/player.html)

1. Open both apps in separate browser windows
2. Click the player app to allow audio
3. In the control apop, click a video tpo play or modify the timer 

### Game Design

Original design drawing includes puzzles and location of key LEGO® components. 

[![LKYSTEX Original Design](images/design-low.png)](images/design-high.png)

> <small>LEGO® is a trademark of the LEGO Group of companies which does not sponsor, authorize or endorse this site.</small>

---

## Make Contact

Reach out to request a custom interactive LEGO® experience:

<form id="contactForm" action="#" method="post" style="max-width:800px;">
    <label for="name">Name:</label><br>
    <input type="text" id="name" name="name">
    <br>
    <label for="email">Email:</label><br>
    <input type="email" id="email" name="email">
    <br>
    <label for="message">Message:</label><br>
    <textarea id="message" name="message" rows="5"></textarea>
    <br>
    <button type="submit">Send</button>
</form>

<div class="components" id="resources">--resources--</div>
<script src="https://cdn.codeadam.ca/components@1.0.0/components.js"></script>

---

<a href="https://codeadam.ca">
<img src="https://cdn.codeadam.ca/images@1.0.0/codeadam-logo-coloured-horizontal.png" width="100">
</a>

<style>
button {
    background: #0366d6;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 1em;
    cursor: pointer;
    transition: background 0.2s;
}

button:hover {
    background: #024ea2;
}

input, textarea {
    border: 2px solid #e1e4e8;
    background: #f6f8fa;
    padding: 5px;
    box-sizing: border-box;
    border-radius: 4px;
    margin-bottom: 8px;
    width: 100%;
    font-size: 1em;
}


</style>
