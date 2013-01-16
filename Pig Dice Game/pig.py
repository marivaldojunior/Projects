"""The Game of Pig"""
# Names: Gavin Chu & Eric O'neill
# Section 19

from dice import make_fair_die, make_test_die
from ucb import main, trace, log_current_line, interact

goal = 100  # The goal of pig is always to score 100 points.

# Taking turns

def roll(turn_total, outcome):
    """Performs the roll action, which adds outcome to turn_total, or loses the
    turn on outcome == 1.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll (the number generated by the die)

    Returns three values in order:
    - the number of points the player scores after the roll
      Note: If the turn is not over after this roll, this return value is 0.
            No points are scored until the end of the turn.
    - the player turn point total after the roll
    - a boolean; whether or not the player's turn is over
    
    >>> roll(7, 3)
    (0, 10, False)
    >>> roll(99, 1)
    (1, 0, True)
    """
    "*** YOUR CODE HERE ***"
    total = turn_total
    if outcome == 1:
        return 1, 0, True
    else:
        total = turn_total + outcome
        return 0, total, False

def hold(turn_total, outcome):
    """Performs the hold action, which adds turn_total to the player's score.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll, ie. the number generated by the die

    Returns three values in order:
    - the number of points the player scores after holding
    - the player turn total after the roll (always 0)
    - a boolean; whether or not the player's turn is over
    
    >>> hold(99, 1)
    (99, 0, True)
    """
    "*** YOUR CODE HERE ***"
    return turn_total, 0, True

def take_turn(plan, dice=make_fair_die(), who='Someone', comments=False):
    """Simulate a single turn and return the points scored for the whole turn.

    Important: The d function should be called once, **and only once**, for
               every action taken!  Testing depends upon this fact.
    
    Arguments:
    plan -- a function that takes the turn total and returns an action function
    dice -- a function that takes no args and returns an integer outcome.
            Note: dice is non-pure!  Call it exactly once per action.
    who -- name of the current player
    comments -- a boolean; whether commentary is enabled
    """
    score_for_turn = 0  # Points scored in the whole turn
    "*** YOUR CODE HERE ***"
    turn_total = 0
    over = False
    while over == False:
        dice_result = dice()
        action = plan(turn_total)
        if action == roll:
            score, turn_total, over = action(turn_total, dice_result)
            if score == 1:
                score_for_turn = 1
            if comments == True:
                commentate(action, dice_result, score_for_turn, turn_total, over, who)
        else:
            score_for_turn = turn_total
            score, turn_total, over = action(turn_total, dice_result)
            if comments == True:
                commentate(action, dice_result, score_for_turn, turn_total, over, who)
    return score_for_turn

def take_turn_test():
    """Test the take_turn function using deterministic test dice."""
    plan = make_roll_until_plan(10)  # plan is a function (see problem 2)
    "*** YOUR CODE HERE ***"
    test_dice = make_test_die(4,6,1)
    assert take_turn(plan, test_dice) == 10, 'score_for_turn should return 10'
    # print(take_turn(plan, test_dice))  # Not deterministic


# Commentating

def commentate(action, outcome, score_for_turn, turn_total, over, who):
    """Print descriptive comments about a game event.
    
    action -- the action function chosen by the current player
    outcome -- the outcome of the die roll
    score_for_turn -- the points scored in this turn by the current player
    turn_total -- the current turn total
    over -- a boolean that indicates whether the turn is over
    who -- the name of the current player 
    """
    print(draw_number(outcome))
    print(who, describe_action(action))
    if over:
        print(who, 'scored', score_for_turn, 'point(s) on this turn.')
    else:
        print(who, 'now has a turn total of', turn_total, 'point(s).')

def describe_action(action):
    """Generate a string that describes an action.

    action -- a function, which should be either hold or roll    

    If action is neither the hold nor roll function, the description should
    announce that cheating has occurred.

    >>> describe_action(roll)
    'chose to roll.'
    >>> describe_action(hold)
    'decided to hold.'
    >>> describe_action(commentate)
    'took an illegal action!'
    """
    "*** YOUR CODE HERE ***"
    if action == roll:
        return 'chose to roll.'
    elif action == hold:
        return 'decided to hold.'
    else:
        return 'took an illegal action!'
    return 'did something...'
 
def draw_number(n, dot='*'):
    """Return an ascii art representation of rolling the number n.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------
    """
    "*** YOUR CODE HERE ***"
    if n == 1:
        action = draw_die(True, False, False, False, dot)
    elif n == 2:
        action = draw_die(False, True, False, False, dot)
    elif n == 3:
        action = draw_die(True, True, False, False, dot)
    elif n == 4:
        action = draw_die(False, True, True, False, dot)
    elif n == 5:
        action = draw_die(True, True, True, False, dot)
    else:
        action = draw_die(False, True, True, True, dot)
    return action

def draw_die(c, f, b, s, dot):
    """Return an ascii art representation of a die.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.
    
     -------
    | b   f |
    | s c s |
    | f   b |
     -------    

    Note: The sides with 2 and 3 dots have 2 possible depictions due to
          rotation. Either representation is acceptable. 

    Note: This function uses Python syntax not yet covered in the course.
    
    c, f, b, s -- booleans; whether to place dots in corresponding positions
    dot        -- A length-one string to use for a dot
    """
    border = ' -------'
    def draw(b): 
        return dot if b else ' '
    c, f, b, s = map(draw, [c, f, b, s])
    top =    ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c,   s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

def play(strategy, opponent_strategy):
    """Simulate a game and return 0 if the first player wins and 1 otherwise.
    
    strategy -- The strategy function for the first player (who plays first)
    opponent_strategy -- The strategy function for the second player
    """
    who = 0 # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    score1, score2 = 0, 0
    win = False
    while win == False:
        if who == 0:
            plan1 = strategy(score1, score2)
            if score1 <= 100:
                if (score1+score2)%7 == 0:
                    die = make_fair_die(4)
                else:
                    die = make_fair_die()
                score_for_turn = take_turn(plan1, die, 'player 1', False)
                score1 = score1 + score_for_turn
                if score1 >= 100:
                    win = True
                    who = other(who)
            who = other(who)
        else:
            plan2 = opponent_strategy(score2, score1)
            if score2 <= 100:
                if (score1+score2)%7 == 0:
                    die = make_fair_die(4)
                else:
                    die = make_fair_die()
                score_for_turn = take_turn(plan2, die, 'player 2', False)
                score2 = score2 + score_for_turn
                if score2 >= 100:
                    win = True
                    who = other(who)
            who = other(who)
    return who

def other(who):
    """Return the other player, for players numbered 0 and 1.
    
    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2


# Basic Strategies

def make_roll_until_plan(turn_goal=20):
    """Return a plan to roll until turn total is at least turn_goal."""
    def plan(turn):
        if turn >= turn_goal:
            return hold
        else:
            return roll
    return plan

def make_roll_until_strategy(turn_goal):
    """Return a strategy to always adopt a plan to roll until turn_goal.
    
    A strategy is a function that takes two game scores as arguments and
    returns a plan (which is a function from turn totals to actions).
    """
    "*** YOUR CODE HERE ***"
    def strategy(score1, score2):
        return make_roll_until_plan(turn_goal)
    return strategy

def make_roll_until_strategy_test():
    """Test that make_roll_until_strategy gives a strategy that returns correct
    roll-until plans."""
    strategy = make_roll_until_strategy(15)    
    plan = strategy(0, 0)
    assert plan(14) == roll, 'Should have returned roll'
    assert plan(15) == hold, 'Should have returned hold'
    assert plan(16) == hold, 'Should have returned hold'


# Experiments (Phase 2)

def average_value(fn, num_samples):
    """Compute the average value returned by fn over num_samples trials.
    
    >>> d = make_test_die(1, 3, 5, 7)
    >>> average_value(d, 100)
    4.0
    """
    "*** YOUR CODE HERE ***"
    k = 1
    result = fn()
    while k < num_samples:
        result = result + fn()
        k = k+1
    average = result/num_samples
    return average

def averaged(fn, num_samples=100):
    """Return a function that returns the average_value of fn when called.

    Note: To implement this function, you will have to use *args syntax, a new
          Python feature introduced in this project.  See the project
          description for details.

    >>> die = make_test_die(3, 1, 5, 7)
    >>> avg_die = averaged(die)
    >>> avg_die()
    4.0
    >>> avg_turn = averaged(take_turn)
    >>> avg_turn(make_roll_until_plan(4), die, 'The player', False)
    3.0

    In this last example, two different turn scenarios are averaged.  
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 (then holds on the 7), scoring 5.
    Thus, the average value is 3.0

    Note: If this last test is called with comments=True in take_turn, the
    doctests will fail because of the extra output.
    """
    "*** YOUR CODE HERE ***"
    def average(*args):
        result = 0
        k = 1
        while k <= num_samples:
            result = result + fn(*args)
            k = k+1
        return result/num_samples
    return average

def compare_strategies(strategy, baseline=make_roll_until_strategy(20)):
    """Return the average win rate (out of 1) of strategy against baseline."""
    as_first = 1 - averaged(play)(strategy, baseline)
    as_second = averaged(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for make_strategy to use against
    the roll-until-20 baseline, between lower_bound and upper_bound (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range
    upper_bound -- upper bound of the evaluation range
    """
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print(value, 'win rate against the baseline:', win_rate) 
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_strategy_experiments():
    """Run a series of strategy experiments and report results."""
    "*** YOUR CODE HERE ***"
    experiment1 = eval_strategy_range(make_roll_until_strategy, 15, 25)
    experiment2 = eval_strategy_range(make_die_specific_strategy, 5, 15)
    experiment3 = eval_strategy_range(make_pride_strategy, 0, 10)
    return experiment1, experiment2, experiment3

def make_die_specific_strategy(four_side_goal, six_side_goal=20):
    """Return a strategy that returns a die-specific roll-until plan.
    
    four_side_goal -- the roll-until goal whenever the turn uses a 4-sided die
    six_side_goal -- the roll-until goal whenever the turn uses a 6-sided die

    """
    "*** YOUR CODE HERE ***"
    def strategy(score1, score2):
        added_score = score1 + score2
        if added_score % 7 == 0:
            return make_roll_until_plan(four_side_goal)
        else:
            return make_roll_until_plan(six_side_goal)
    return strategy

def make_pride_strategy(margin, turn_goal=20):
    """Return a strategy that wants to finish a turn winning by at least margin.

    margin -- the size of the lead that the player requires
    turn_goal -- the minimum roll-until turn goal, even when winning
    """
    "*** YOUR CODE HERE ***"
    def strategy(score1, score2):
        score_needed = score2 - score1 + margin
        if score_needed > turn_goal:
            return make_roll_until_plan(score_needed)
        else:
            return make_roll_until_plan(turn_goal)
    return strategy

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    1. start off with turn goal = 20 for six-sided die and 7 for four-sided die
    2. final strategy consists of a series of conditions depending on the scores for each player after each turn
    3. if score needed to reach 100 points is less than turn goal of 20,
       turn goal becomes the score needed to reach exactly 100 points
    4. if opponent can win in the next turn, just keep rolling hoping the player wins before the turn is passed
    5. if player is behind by at least 10 points, roll more aggressively
    6. turn goal changes according to how many points is needed to make the combine score of both player
       equal to a multiple of 7, which gives the opponent a four-sided die
    returns a strategy that returns a plan
    """
    "*** YOUR CODE HERE ***"
    turn_goal = 20
    four_side_goal = 7
    added_score = score + opponent_score
    score_difference = opponent_score - score
    score_until_win = 100 - score
    score_until_opp_win = 100 - opponent_score

    
    if score_until_win < 20 or score_until_opp_win <= 20:
        return make_roll_until_plan(score_until_win)
    #behind by 10 points
    elif score_difference > 10:
        def plan(turn):
            if added_score%7 == 0:
                turn_goal = 14
            elif added_score%7 == 3:
                turn_goal = 25
            elif added_score%7 == 4:
                turn_goal = 24
            elif added_score%7 == 5:
                turn_goal = 23
            elif added_score%7 == 6:
                turn_goal = 22
        return make_roll_until_plan(turn_goal)
    elif added_score%7 ==0:
        return make_roll_until_plan(four_side_goal)
    elif added_score%7 == 1:
        return make_roll_until_plan(20)
    elif added_score%7 == 2:
        return make_roll_until_plan(19)
    elif added_score%7 == 3:
        return make_roll_until_plan(18)
    elif added_score%7 == 4:
        return make_roll_until_plan(17)
    elif added_score%7 == 5:
        return make_roll_until_plan(23)
    elif added_score%7 == 6:
        return make_roll_until_plan(22)
    elif score > 75:
        return make_roll_until_plan(24)
    else:
        return make_roll_until_plan(turn_goal)
    return strategy

def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive plan.
    
    Note: this function uses Python syntax not yet covered in the course.
    """
    print('You have', score, 'and they have', opponent_score, 'total score')
    def plan(turn):
        if turn > 0:
            print('You now have a turn total of', turn, 'points')
        while True:
            response = input('(R)oll or (H)old?')
            if response.lower()[0] == 'r':
                return roll
            elif response.lower()[0] == 'h':
                return hold
            print('Huh?')
    return plan

@main
def run():
    take_turn_test()
    # play(final_strategy, make_roll_until_strategy(20))

    # Uncomment the next line to play an interactive game
    # play(interactive_strategy, make_roll_until_strategy(20))

    # Uncomment the next line to test make_roll_until_strategy
    run_strategy_experiments()

    print(averaged(compare_strategies)(final_strategy))
    
    print(compare_strategies(final_strategy))
    

