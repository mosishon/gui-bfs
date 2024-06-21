import collections


Point = collections.namedtuple("Point",['x','y'])
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()
    

class Block:
    all_blocks: list["Block"] = []

    def __init__(self, x: int, y: int, is_valid: bool):
        self.x = x
        self.y = y
        self.is_valid = is_valid
        self.all_blocks.append(self)

    @property
    def right_block(self) -> "Block":
        for block in self.all_blocks:
            if block.x == self.x + 1 and block.y == self.y:
                return block
        return None

    @property
    def left_block(self) -> "Block":
        for block in self.all_blocks:
            if block.x == self.x - 1 and block.y == self.y:
                return block
        return None

    @property
    def top_block(self) -> "Block":
        for block in self.all_blocks:
            if block.x == self.x and block.y == self.y + 1:
                return block
        return None

    @property
    def bottom_block(self) -> "Block":
        for block in self.all_blocks:
            if block.x == self.x and block.y == self.y - 1:
                return block
        return None

    @staticmethod
    def get_block(point:Point):
        for block in Block.all_blocks:
            if block.x == point.x and block.y == point.y:
                return block
        return None

    @property
    def neighbors(self):
        return tuple(filter(lambda x: x, (
            self.get_block(Point(self.x + 1, self.y)),
            self.get_block(Point(self.x, self.y-1)),
            self.get_block(Point(self.x, self.y+1)),
            self.get_block(Point(self.x-1, self.y)),
            # self.get_block(Point(self.x-1, self.y+1)),
            # self.get_block(Point(self.x-1, self.y-1)),
            # self.get_block(Point(self.x + 1, self.y+1)),
            # self.get_block(Point(self.x + 1, self.y-1)),


            )))

    def __str__(self) -> str:
        return f"Block(x={self.x}, y={self.y}, valid={self.is_valid})"

    def __repr__(self) -> str:
        return self.__str__()


class Agent:
    def __init__(self, start_block: Block):
        self.start_block = start_block
        self.current_block = start_block
    @property
    def neighbors_block(self):
        return self.current_block.neighbors

    def start_moving(self, target:Block):
        possible_moves = Queue()
        possible_moves.put(self.start_block)
        addresses = {}
        addresses[self.start_block] = None

        while not possible_moves.empty():
            location:Block = possible_moves.get()
            if location == target:
                print("FOUND THE TARGET")
                break
            for next_move in location.neighbors:
                if next_move not in addresses and next_move.is_valid:
                    possible_moves.put(next_move)
                    addresses[next_move] = location
                    
        return addresses
    
        
    def move_to(self, block: Block):
        print(f"[!] Player Moves to {block}")
        self.current_block = block


def create_matrix(x:int, y:int):
    Block.all_blocks = []
    for i in range(x):
        for ii in range(y):
            Block(i, ii, True)

def ban_blocks(points:list[Point]):
    for point in points:
        if block:=Block.get_block(point):
            block.is_valid = False


if __name__ == '__main__':
    create_matrix(5,5)
    ban_blocks([Point(1,4),Point(1,3),Point(1,2),Point(1,1),Point(3,0),Point(3,1),Point(3,2),Point(3,3)])


    to_find = Block.get_block(Point(4,0))
    player = Agent(Block.get_block(Point(0,4)))
    print("Finding :",to_find)
    paths = player.start_moving(to_find)


    found = False
    while not found: 
        print(to_find)
        prev = paths[to_find]
        if prev == player.start_block:
            break
        to_find = prev
        

