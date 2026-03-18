# I AM NOT DONE

"""
con07_actor_model.py

The Actor Model is a concurrency paradigm where "actors" are independent
entities that communicate only through message passing. Each actor has its
own mailbox and processes messages sequentially, eliminating shared state.

Your task: Implement a basic actor system with message passing.

Key concepts:
- Actors: Independent entities with state and behavior
- Mailboxes: Message queues for each actor
- Message passing: Asynchronous communication
- No shared state: Actors only communicate via messages
"""

from collections import deque
from typing import Dict, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import unittest


ActorId = int
MessageId = int


@dataclass
class Message:
    """Represents a message between actors."""
    id: MessageId
    sender: ActorId
    recipient: ActorId
    content: str


class Mailbox:
    """Message queue for an actor."""

    def __init__(self):
        self.messages = deque()

    def send(self, message: Message) -> None:
        """
        TODO: Add a message to the mailbox.

        Args:
            message: The message to add
        """
        pass  # TODO: Implement this

    def receive(self) -> Optional[Message]:
        """
        TODO: Remove and return the next message from the mailbox.

        Returns:
            The next message, or None if empty
        """
        pass  # TODO: Implement this

    def __len__(self) -> int:
        """Get the number of messages in the mailbox."""
        return len(self.messages)

    def is_empty(self) -> bool:
        """Check if the mailbox is empty."""
        return len(self.messages) == 0


class Actor(ABC):
    """Abstract base class for actors."""

    def __init__(self, actor_id: ActorId):
        self.actor_id = actor_id

    @abstractmethod
    def receive(self, message: Message, system: 'ActorSystem') -> None:
        """
        Handle a received message.

        Args:
            message: The message to handle
            system: The actor system for sending messages
        """
        pass


class ActorSystem:
    """System for managing actors and message passing."""

    def __init__(self):
        self.mailboxes: Dict[ActorId, Mailbox] = {}
        self.next_message_id = 0
        self.delivered_messages: List[Message] = []

    def register_actor(self, actor_id: ActorId) -> None:
        """
        TODO: Register a new actor by creating its mailbox.

        Args:
            actor_id: The actor to register
        """
        pass  # TODO: Implement this

    def send_message(self, sender: ActorId, recipient: ActorId, content: str) -> MessageId:
        """
        TODO: Send a message from one actor to another.

        Steps:
        1. Create a new message with a unique ID
        2. Add it to the recipient's mailbox
        3. Increment next_message_id
        4. Return the message ID

        Args:
            sender: Sending actor ID
            recipient: Receiving actor ID
            content: Message content

        Returns:
            The message ID
        """
        pass  # TODO: Implement this

    def deliver_message(self, actor: Actor) -> bool:
        """
        TODO: Deliver one message to the given actor.

        Steps:
        1. Get the actor's mailbox
        2. Receive a message from the mailbox
        3. Call actor.receive() with the message
        4. Record the message in delivered_messages
        5. Return True if a message was delivered, False otherwise

        Args:
            actor: The actor to deliver to

        Returns:
            True if message delivered, False otherwise
        """
        pass  # TODO: Implement this

    def run_until_idle(self, actors: Dict[ActorId, Actor]) -> None:
        """
        TODO: Keep delivering messages until all mailboxes are empty.

        Process actors in round-robin fashion.

        Args:
            actors: Dictionary of actor ID to actor instance
        """
        pass  # TODO: Implement this

    def has_pending_messages(self, actor_id: ActorId) -> bool:
        """Check if an actor has pending messages."""
        mailbox = self.mailboxes.get(actor_id)
        return mailbox is not None and not mailbox.is_empty()

    def get_delivered_messages(self) -> List[Message]:
        """Get all delivered messages."""
        return self.delivered_messages


# Example actor implementations for testing


class EchoActor(Actor):
    """Actor that echoes messages back to sender."""

    def __init__(self, actor_id: ActorId):
        super().__init__(actor_id)
        self.echo_count = 0

    def receive(self, message: Message, system: ActorSystem) -> None:
        """
        TODO: Echo the message back to the sender.

        Prepend "Echo: " to the content.
        """
        pass  # TODO: Implement this


class CounterActor(Actor):
    """Actor that counts increment messages."""

    def __init__(self, actor_id: ActorId):
        super().__init__(actor_id)
        self.count = 0

    def receive(self, message: Message, system: ActorSystem) -> None:
        """
        TODO: Increment counter based on message content.

        If message content is "increment", increment count.
        """
        pass  # TODO: Implement this


class ForwarderActor(Actor):
    """Actor that forwards messages to another actor."""

    def __init__(self, actor_id: ActorId, forward_to: ActorId):
        super().__init__(actor_id)
        self.forward_to = forward_to

    def receive(self, message: Message, system: ActorSystem) -> None:
        """
        TODO: Forward the message to the designated actor.

        Append " (forwarded)" to the content.
        """
        pass  # TODO: Implement this


class TestActorModel(unittest.TestCase):
    """Test cases for Actor Model."""

    def test_basic_message_passing(self):
        """Test basic message sending."""
        system = ActorSystem()
        system.register_actor(1)
        system.register_actor(2)

        msg_id = system.send_message(1, 2, "Hello")

        self.assertEqual(msg_id, 0)
        self.assertTrue(system.has_pending_messages(2))
        self.assertFalse(system.has_pending_messages(1))

    def test_echo_actor(self):
        """Test echo actor functionality."""
        system = ActorSystem()
        actors: Dict[ActorId, Actor] = {}

        echo = EchoActor(1)
        system.register_actor(1)
        system.register_actor(2)
        actors[1] = echo

        system.send_message(2, 1, "Test")
        system.deliver_message(echo)

        # Should have sent echo back to actor 2
        self.assertTrue(system.has_pending_messages(2))

    def test_counter_actor(self):
        """Test counter actor functionality."""
        system = ActorSystem()
        system.register_actor(1)
        system.register_actor(2)

        counter = CounterActor(1)

        system.send_message(2, 1, "increment")
        system.send_message(2, 1, "increment")
        system.send_message(2, 1, "increment")

        system.deliver_message(counter)
        system.deliver_message(counter)
        system.deliver_message(counter)

        self.assertEqual(counter.count, 3)

    def test_message_forwarding(self):
        """Test message forwarding."""
        system = ActorSystem()
        system.register_actor(1)
        system.register_actor(2)
        system.register_actor(3)

        forwarder = ForwarderActor(2, 3)

        system.send_message(1, 2, "Forward this")
        system.deliver_message(forwarder)

        # Should have forwarded to actor 3
        self.assertTrue(system.has_pending_messages(3))

    def test_multiple_messages_fifo(self):
        """Test messages are delivered in FIFO order."""
        system = ActorSystem()
        system.register_actor(1)
        system.register_actor(2)

        system.send_message(1, 2, "First")
        system.send_message(1, 2, "Second")
        system.send_message(1, 2, "Third")

        counter = CounterActor(2)

        system.deliver_message(counter)
        delivered = system.get_delivered_messages()
        self.assertEqual(delivered[0].content, "First")

        system.deliver_message(counter)
        delivered = system.get_delivered_messages()
        self.assertEqual(delivered[1].content, "Second")

    def test_run_until_idle(self):
        """Test running until all messages are processed."""
        system = ActorSystem()
        actors: Dict[ActorId, Actor] = {}

        system.register_actor(1)
        system.register_actor(2)
        actors[1] = CounterActor(1)
        actors[2] = CounterActor(2)

        system.send_message(0, 1, "increment")
        system.send_message(0, 2, "increment")
        system.send_message(0, 1, "increment")

        system.run_until_idle(actors)

        # All messages should be delivered
        self.assertFalse(system.has_pending_messages(1))
        self.assertFalse(system.has_pending_messages(2))
        self.assertEqual(len(system.get_delivered_messages()), 3)

    def test_message_chain(self):
        """Test chain of message forwarding."""
        system = ActorSystem()
        actors: Dict[ActorId, Actor] = {}

        system.register_actor(1)
        system.register_actor(2)
        system.register_actor(3)

        actors[1] = ForwarderActor(1, 2)
        actors[2] = ForwarderActor(2, 3)
        actors[3] = CounterActor(3)

        system.send_message(0, 1, "Start")
        system.run_until_idle(actors)

        # Message should have been forwarded through the chain
        delivered = system.get_delivered_messages()
        self.assertGreaterEqual(len(delivered), 3)

    def test_mailbox_fifo(self):
        """Test mailbox FIFO ordering."""
        mailbox = Mailbox()

        msg1 = Message(0, 1, 2, "First")
        msg2 = Message(1, 1, 2, "Second")
        msg3 = Message(2, 1, 2, "Third")

        mailbox.send(msg1)
        mailbox.send(msg2)
        mailbox.send(msg3)

        self.assertEqual(mailbox.receive(), msg1)
        self.assertEqual(mailbox.receive(), msg2)
        self.assertEqual(mailbox.receive(), msg3)

    def test_empty_mailbox(self):
        """Test receiving from empty mailbox."""
        mailbox = Mailbox()

        result = mailbox.receive()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
