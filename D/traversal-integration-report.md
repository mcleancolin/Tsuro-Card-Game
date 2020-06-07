1. How well did the other team implement your specification? Did they follow it truthfully? If they deviated from it, was it well justified?

Our spec was very open ended, and they implemented it as it was written. They implemented all three functions and each of the data types (as described). The only thing they missed was the axiom, “There is at most one edge between each node”. Because our spec was so open ended, I think that lead to slight miscommunication on the implementation on two of our methods; Our assumption was that all of these methods would be mutating and interacting with a graph, rather than the nodes. There is a difference between calling new_labrinyth and the constructor - both return a graph after taking a list of names, but one turns those strings into nodes and one keeps them as strings in the same field. This is confusing because graphs will exist in two states.

2. Were you or would you be able to integrate the received implementation with your client module from Task 3 of Assignment C? What was the actual or what is estimated effort required?

As it stands, we would not be able to integrate the implementation we received as they had interpreted our spec slightly differently. We estimate it would take us around a day to refactor the code so those pieces can be integrated.

3. Based on the artifact you received and the above two questions, how could you improve your specification to make it more amenable for implementation as you intended?

We should have clarified that we meant for the functions to be acting on the graph rather than individual nodes. More explanation on our assumptions would have helped the other team implement our spec as we imagined.
