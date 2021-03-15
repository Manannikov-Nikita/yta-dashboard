

# YouTube analytics views graph

**The Challenge:**

Our client has an active YouTube channel [https://www.youtube.com/channel/UCM6ae9jypjFjrprCy_HqWCg](https://www.youtube.com/channel/UCM6ae9jypjFjrprCy_HqWCg)
We need to analyze historical data on the number of views of this video [https://www.youtube.com/watch?v=-_5iXPvveAY](https://www.youtube.com/watch?v=-_5iXPvveAY) and build a simple time graph with a filter by date
___

**Graph builded on generated(synth) data** 

![alt text](https://sun9-45.userapi.com/impf/cE6pHLkCQXN5xzR0nJG9Pnp8rMeZhPU7wv8WLQ/LhSArXzd1Ns.jpg?size=1052x515&quality=96&sign=433c6c3b4145122c037784cba827ab37&type=album)
**Application run on a test youtube channel**

(https://user-images.githubusercontent.com/55488385/111140609-97e53600-8593-11eb-814a-afddf3412870.mp4)

**Known issues**
1. Connection to API is unstable, each time app trys to update graph it requests data from api and user need to manualy authorize it. (Shown on the viedo)
2. For some reason API cant respond data for few last days. I have tested this on API Explorer on official API documentation, so i dont think that it is my mistake. 


