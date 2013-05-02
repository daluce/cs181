import common
import game_interface
import random
import time
import copy
import modelfree
from data_reader import *
from __init__ import *

ATE_NUTRITIOUS = 0
ATE_POISONOUS = 1
SEEN_NOTHING = 2
PASSED = 3

#def get_move(view):
#  #return common.get_move(view)
#  return common.get_move(view,"images1.txt","value1.txt")

def get_move(view):
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

  cur_life = view.GetLife()
  
  if hasattr(view, 'previous_life'):
    diff = cur_life - view.previous_life
    view.previous_life = cur_life
  else:
    diff = 0

  cur_state = 0
  if hasattr(view, 'old_hasPlant'):
    if view.old_hasPlant == 0:
      cur_state = SEEN_NOTHING
    elif view.ate == 0:
      cur_state = PASSED
    elif diff < 0:
      cur_state = ATE_POISONOUS
    elif diff > 1:
      cur_state = ATE_NUTRITIOUS
  else:
    cur_state = PASSED

  view.old_hasPlant = hasPlant

  if hasattr(view, 'prev_state'):
    modelfree.Q_learn_it(q_table, view.prev_state, view.prev_action, cur_state, diff)

  eat = -1
  if hasPlant:
    eat = -1  
    nutritious_count = 0
    while (eat == -1):
      unprocessed_image = view.GetImage()
      image = DataReader.ConvertTuple(unprocessed_image)
      if network.Classify(image):
        nutritious_count += 1
      else:
        nutritious_count -= 1

      if nutritious_count == 2:
        eat = 1
      elif nutritious_count == -2:
        eat = 0

  view.ate = eat
  view.prev_state = cur_state
  view.prev_action = modelfree.Q_get_move(q_table,cur_state)

  modelfree.Writeout_Q_table(q_table)
  #time.sleep(0.1)
  return (view.prev_action, eat)
  #return (1, eat)
