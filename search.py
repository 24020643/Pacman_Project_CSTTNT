# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # 1. Tạo Stack (ngăn xếp) để lưu các điểm cần đi.
    # Cơ chế LIFO (vào sau ra trước) của Stack chính là thứ tạo nên "tính đi sâu" của DFS.
    s = util.Stack()
    # 2. Đẩy điểm xuất phát vào Stack.
    # Phần tử lưu dưới dạng Tuple: (Trạng thái hiện tại, Danh sách hành động đã đi tới đây).
    # Ban đầu ở vạch xuất phát thì danh sách bước đi là rỗng [].
    s.push((problem.getStartState(), []))
    # 3. Dùng tập hợp (Set) để ghi nhớ những điểm ĐÃ XỬ LÝ xong.
    # Set cho tốc độ tìm kiếm cực nhanh O(1).
    seen = set()
    # 4. Vòng lặp chạy liên tục cho đến khi Stack không còn gì để rút (hết đường đi)
    while not s.isEmpty():
        # Lấy phần tử nằm trên ĐỈNH Stack ra (mới nhất)
        curr, path = s.pop()
        # Nếu điểm này đã từng bị rút ra và xử lý trước đó rồi -> Bỏ qua
        if curr in seen:
            continue
        # Đánh dấu chính thức: "Tôi đang đứng xử lý điểm curr này"
        seen.add(curr)
        # Kiểm tra xem điểm này có phải Đích không
        # Nếu đúng -> Trả về ngay danh sách các bước đi (path) để tới được đây
        if problem.isGoalState(curr):
            return path
        # Tìm tất cả các điểm hàng xóm có thể đi tới từ curr
        # getSuccessors trả về (Trạng thái kế tiếp, Hành động, Chi phí)
        for nxt, act, _ in problem.getSuccessors(curr):
            # Nếu điểm hàng xóm chưa từng được xử lý
            if nxt not in seen:
                # Đẩy điểm đó vào Stack.
                # Đường đi mới = đường đi cũ + bước đi mới (path + [act])
                s.push((nxt, path + [act]))
    # Trường hợp đã đi hết tất cả các ngách mà không thấy đích
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Tạo hàng đợi cho BFS
    frontier = util.Queue()
    start_state = problem.getStartState()
    frontier.push((start_state, []))

    # Theo dõi các trạng thái đã xét để tránh lặp vô hạn
    visited = {start_state}

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        # Nếu đã đến đích thì trả về đường đi
        if problem.isGoalState(state):
            return actions

        # Xét các trạng thái kế tiếp
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                frontier.push((successor, actions + [action]))

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = set()

    fringe.push((problem.getStartState(), []), 0)

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions
        
        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    new_actions = actions + [action]
                    # tieu chi de danh gia xem dinh nao duoc xet tiep theo
                    new_cost = problem.getCostOfActions(new_actions) 
                    fringe.push((successor, new_actions), new_cost)

    return []  
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue() # Bien tim kiem
    visited = set() # closed set luu nhung dinh da duoc xet qua

    start_state = problem.getStartState()
    fringe.push((start_state, []), heuristic(start_state, problem))

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state) # Dannh dau da tham
            # Xet dinh ke chua tham
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:

                    g_cost = problem.getCostOfActions(actions + [action])
                    h_cost = heuristic(successor, problem)
                    f_cost = g_cost + h_cost

                    fringe.push((successor, actions + [action]), f_cost)

    return []  # Truong hop ko tim thay duong di
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
