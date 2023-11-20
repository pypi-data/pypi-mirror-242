from collections import deque
from pyglet.event import EventDispatcher


class TurnManager(EventDispatcher):
    EventDispatcher.register_event_type('on_turn_change')
    EventDispatcher.register_event_type('on_turn_record')
    """TurnManager class
    
    This class is used to manage the turn order of the demo. It is used to
    determine which charactor is currently active and which charactor is next in line.
    
    Attributes:
        window (Window): The window object.
        current_turn (int): The current turn number.
        current_actor (_BaseActor): The current charactor.
        actor_list (list): A list of all actors in the demo.
        turn_queue (list): A list of actors in turn order.
        turn_queue_index (int): The index of the current charactor in the turn queue.
        turn_queue_length (int): The length of the turn queue.
        turn_queue_dirty (bool): Whether the turn queue needs to be sorted.
        turn_queue_sorted (bool): Whether the turn queue is sorted.
        
    Methods:
        create_queue: Creates a turn queue from the charactor list.
        add_actor: Adds an charactor to the charactor list.
        remove_actor: Removes an charactor from the charactor list.
        get_actor_list: Returns the charactor list.
        get_current_actor: Returns the current charactor.
        get_current_turn: Returns the current turn number.
        get_turn_queue: Returns the turn queue.
        get_turn_queue_index: Returns the turn queue index.
        get_turn_queue_length: Returns the turn queue length.
        get_turn_queue_dirty: Returns the turn queue dirty flag.
        get_turn_queue_sorted: Returns the turn queue sorted flag.
        set_current_actor: Sets the current charactor.
        set_current_turn: Sets the current turn number.
        set_turn_queue: Sets the turn queue.
        set_turn_queue_index: Sets the turn queue index.
        set_turn_queue_length: Sets the turn queue length.
        set_turn_queue_dirty: Sets the turn queue dirty flag.
        set_turn_queue_sorted: Sets the turn queue sorted flag.
        sort_turn_queue: Sorts the turn queue.
        next_turn: Increments the turn number and returns the next charactor.
        reset: Resets the turn manager.
        
        """

    def __init__(self, first_player=None, second_player=None, length=10000):
        super(TurnManager, self).__init__()
        self.current_turn_number = 0
        self.current_round_number = 0
        self.current_actor = None
        self.current_turn = None
        self.actor_list = []
        self.turn_queue = deque()
        self.turn_queue_index = 0
        self.turn_queue_length = length
        self.turn_queue_dirty = False
        self.turn_queue_sorted = False
        self.turn_history = []
        self.turn_record = TurnRecord()
        if first_player is not None:
            self.add_actor(first_player)
        if second_player is not None:
            self.add_actor(second_player)
        if self.actor_list != []:
            self.finalize()

    def create_queue(self):
        self.turn_queue.extend(self.actor_list * (self.turn_queue_length // len(self.actor_list)))  
        self.turn_queue_dirty = True
        self.turn_queue_sorted = True

    def add_actor(self, actor, index=None):
        if index is not None:
            self.actor_list.insert(index, actor)
        else:
            self.actor_list.append(actor)
        self.turn_queue_dirty = True

    def remove_actor(self, actor):
        self.actor_list.remove(actor)
        self.turn_queue_dirty = True

    def finalize(self):
        self.create_queue()
        self.set_current_actor(self.turn_queue.popleft())
        current_actor = self.get_current_actor()
        current_actor._is_turn = True
        self.set_current_turn_number(0)
        self.current_turn = Turn(self.current_turn_number, self.current_actor, self.turn_record)
        self._set_handler('on_turn_change', self.current_actor._on_turn_change)
        self._set_handler('on_turn_record', self.current_turn.record)

    def get_actor_list(self):
        return self.actor_list

    def get_current_actor(self):
        return self.current_actor

    def get_current_turn_number(self):
        return self.current_turn_number

    def get_turn_queue(self):
        return self.turn_queue

    def get_turn_queue_index(self):
        return self.turn_queue_index

    def get_turn_queue_length(self):
        return self.turn_queue_length

    def get_turn_queue_dirty(self):
        return self.turn_queue_dirty

    def get_turn_queue_sorted(self):
        return self.turn_queue_sorted

    def set_current_actor(self, actor):
        self.current_actor = actor

    def set_current_turn_number(self, turn):
        self.current_turn_number = turn
        if self.current_turn_number % self.turn_queue_length == 0:
            self.current_round_number += 1

    def set_turn_queue(self, queue):
        self.turn_queue = queue

    def set_turn_queue_index(self, index):
        self.turn_queue_index = index

    def set_turn_queue_length(self, length):
        self.turn_queue_length = length

    def set_turn_queue_dirty(self, dirty):
        self.turn_queue_dirty = dirty

    def set_turn_queue_sorted(self, sorted):
        self.turn_queue_sorted = sorted

    def sort_turn_queue(self):
        sort_list = list(self.turn_queue)
        
        sort_list.sort(key=lambda actor: actor.initiative, reverse=True)
        self.turn_queue = deque(sort_list)
        self.turn_queue_sorted = True

    def next_turn(self, turn_record = None):
        if turn_record is not None:
            self.update_turn_record(turn_record)
        self.turn_history.append(self.current_turn)
        if self.turn_queue_index >= self.turn_queue_length:
            self.turn_queue_index = 0
        else:
            self.turn_queue_index += 1
        self.current_turn_number += 1
        self.dispatch_event('on_turn_change', self.current_actor)
        self.current_actor._is_turn = False
        self.dispatch_event('on_turn_record', self.current_actor.actions)
        self.current_actor = self.turn_queue.popleft()
        self.current_actor._is_turn = True
        self._set_handler('on_turn_change', self.current_actor._on_turn_change)
        self.current_turn = Turn(self.current_turn_number, self.current_actor, self.turn_record)
        self.refresh()

    def update_turn_record(self, turn_record):
        self.turn_record = turn_record

    def reset(self):
        self.current_turn_number = 0
        self.current_actor = None
        self.turn_queue = []
        self.turn_queue_index = 0
        self.turn_queue_length = 0
        self.turn_queue_dirty = False
        self.turn_queue_sorted = False

    def refresh(self):
        for actor in self.actor_list:
            if self.current_actor == actor:
                actor.dispatcher._set_handler('on_turn_end', self.current_turn.record)
        self.current_turn.dispatcher._set_handler('on_turn_record', self.next_turn)


class TurnRecord:
    def __init__(self):
        self.record = {}


class Turn:
    _dispatcher = EventDispatcher()
    _dispatcher.register_event_type('on_turn_record')
    def __init__(self, turn_number=None, actor=None, turn_record=None):
        self._dispatcher.set_handler('on_turn_record', self.record)
        self.turn_number = turn_number if turn_number is not None else 0
        self.actor = actor if actor is not None else None
        self.turn_record = turn_record

    def record(self, actions):
        record = {self.turn_number: {'Actor': self.actor, 'Actions': actions}}
        self.turn_record.record.update(record)
        print(f'turn recorded: {record}')
        self.dispatcher.dispatch_event('on_turn_record', self.turn_record)
