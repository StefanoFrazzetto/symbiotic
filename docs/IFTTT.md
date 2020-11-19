# IFTTT

IFTTT is a platform that allows you to control your smart devices and combine
different online services to automate different tasks. You can find an example 
below on how to create an applet that allows you to control a smart light bulb 
combining SmarterHome and IFTTT.

## Enabling Webhooks

In order to make Webhooks available to your applets, you will need to enable them

1. Visit the [settings page](https://ifttt.com/maker_webhooks/settings) 
2. Click **Connect**
3. Click **Settings**, on the top right side of the page
4. Copy the token, e.g. _https[]()://maker.ifttt.com/use/
**your_webhooks_token**_
5. Paste the token in **config.yaml** in your SmarterHome project

This token will allow SmarterHome to call the webhook(s) on your behalf to 
trigger all the events you have specified.

## Creating an applet for your smart light bulb

Now that you have enabled Webhooks, you can create your first applet. If you don't know what an applet is, you can read more about them on the [IFTTT Help Center page](https://help.ifttt.com/hc/en-us/articles/115010361348-What-is-an-Applet-). In short, an applet is the logic that connects
two (or more) apps or devices together.

The following are the instructions to create an applet to control a KS130 light bulb:

1. Visit the [IFTTT applet page](https://ifttt.com/create)
2. Add the **Webhooks** trigger
   1. Select '**If This**'
   2. Choose '**Webhooks**', then '**Receive a web request**'
   3. Set a sensible name for your event, e.g. *switch_on_light*

3. Add the service and actions that will be triggered by the webhook
   1. Select '**Then That**'
   2. Choose your service, in my case '**TP-Link Kasa**'
   3. Add the '*Turn on*' action
   4. Click '*Create action*'

4. Add another action to change the ligh bulb colour, brightness, etc.
   1. Select the *bottom* plus button (+)
   2. Choose the same service as the previous step
   3. Add the '*Change color*' action
   4. Click '*Create action*'
  
5. Create a '**Filter**' to extract the values from the web request
   1. Select the *top* plus button (+)
   2. Choose '*Add filter*'
   3. Paste the code below into the text area
   4. Click '*Create filter*'

```javascript
var brightness = MakerWebhooks.event.Value1
var color = MakerWebhooks.event.Value2
var transition_duration = MakerWebhooks.event.Value3

Kasa.changeColor.setBrightness(brightness)
Kasa.changeColor.setColor(color)
Kasa.changeColor.setTransitionDuration(transition_duration)
```

5. Give your applet a title, e.g. *Switch on bedroom light through webhook*
6. Click the '*Finish*' button

\
Now that you have created your applet, you will be able to configure SmarterHome
to interact with it.
