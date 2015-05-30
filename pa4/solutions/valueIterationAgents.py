# CSE 150, valueIterationAgents.py
# -----------------------------------------------
# Rene Sanchez A11866286 risanche@ucsd.edu
# Chris Weller A10031853 chriskweller@gmail.com
# -----------------------------------------------
# Description: Implementation of a Value Iteration algorithm that takes a 
# Markov Decision Process as a problem to solve and runs a set amount of 
# iterations and discount factor, returning the best policy obtained
# after said amount of iterations.

import mdp, util

from learningAgents import ValueEstimationAgent

#Class that determines the best policy for a given MDP, discount and number 
# of iterations to test upon.
class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    #Calculates the best policy by the use of the helper methods below
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        U = util.Counter()                  #Set the dict = 0 for all entries
        counter = 0
        
        while self.iterations > counter:    #while haven't done all iterations
            U = util.Counter()              #Set the dict = 0 for all entries
            for s in self.mdp.getStates():
                if self.mdp.isTerminal(s):  #At "end" state
                    U[s] = 0
                else:
                    prevQ = float('-inf')   #Stores previously highest qVal
                    for action in self.mdp.getPossibleActions(s):
                        qVal = 0
                        for pair in self.mdp.getTransitionStatesAndProbs(s,action):
                            tranState = pair[0]     #state we move to
                            prob = pair[1]          #probability of moving there
            
                            reward = self.mdp.getReward(s,action,tranState)
                            maxAction = (self.discount)*(self.values[tranState])
                            qVal += prob*(reward + maxAction)   #Calculate Qvalue
                                                                #using formula
                        U[s] = max(prevQ, qVal)     #Store only the higuest Qval recorded
                        prevQ = U[s]
                        
            self.values = U             #Update utility values for our agent
            counter +=1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qVal = 0
        for pair in self.mdp.getTransitionStatesAndProbs(state,action):
            tranState = pair[0]     #state we move to
            prob = pair[1]          #probability of moving to state
            
            reward = self.mdp.getReward(state,action,tranState)
            maxAction = (self.discount)*(self.values[tranState])
            qVal += prob*(reward + maxAction)   #Calculate Qvalue using formula
            
        return qVal
            
         
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        currActionVal = float('-inf')   #Holds the Qval of current best action
        bestAction = None               #Holds the best action found so far
        
        if self.mdp.isTerminal(state):  #If we are at "end" square
            return None
        
        for action in self.mdp.getPossibleActions(state):
            if self.getQValue(state,action) >= currActionVal: #found better action
                bestAction = action                   #update best action found
                currActionVal = self.getQValue(state,action)
                
        return bestAction
        
    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)
