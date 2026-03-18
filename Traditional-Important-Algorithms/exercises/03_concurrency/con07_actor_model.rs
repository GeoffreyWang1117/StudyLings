// con07_actor_model.rs
//
// The Actor Model is a concurrency paradigm where "actors" are independent
// entities that communicate only through message passing. Each actor has its
// own mailbox and processes messages sequentially, eliminating shared state.
//
// Your task: Implement a basic actor system with message passing.
//
// Key concepts:
// - Actors: Independent entities with state and behavior
// - Mailboxes: Message queues for each actor
// - Message passing: Asynchronous communication
// - No shared state: Actors only communicate via messages

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

pub type ActorId = usize;
pub type MessageId = usize;

#[derive(Debug, Clone, PartialEq)]
pub struct Message {
    pub id: MessageId,
    pub from: ActorId,
    pub to: ActorId,
    pub content: String,
}

impl Message {
    pub fn new(id: MessageId, from: ActorId, to: ActorId, content: String) -> Self {
        Self { id, from, to, content }
    }
}

pub trait Actor {
    fn id(&self) -> ActorId;
    fn receive(&mut self, message: Message, system: &mut ActorSystem);
}

pub struct Mailbox {
    messages: VecDeque<Message>,
}

impl Mailbox {
    pub fn new() -> Self {
        Self {
            messages: VecDeque::new(),
        }
    }

    pub fn send(&mut self, message: Message) {
        // TODO: Add a message to the mailbox
        todo!()
    }

    pub fn receive(&mut self) -> Option<Message> {
        // TODO: Remove and return the next message from the mailbox
        todo!()
    }

    pub fn len(&self) -> usize {
        self.messages.len()
    }

    pub fn is_empty(&self) -> bool {
        self.messages.is_empty()
    }
}

pub struct ActorSystem {
    mailboxes: HashMap<ActorId, Mailbox>,
    next_message_id: MessageId,
    delivered_messages: Vec<Message>,
}

impl ActorSystem {
    pub fn new() -> Self {
        Self {
            mailboxes: HashMap::new(),
            next_message_id: 0,
            delivered_messages: Vec::new(),
        }
    }

    pub fn register_actor(&mut self, actor_id: ActorId) {
        // TODO: Register a new actor by creating its mailbox
        todo!()
    }

    pub fn send_message(&mut self, from: ActorId, to: ActorId, content: String) -> MessageId {
        // TODO: Send a message from one actor to another
        // 1. Create a new message with a unique ID
        // 2. Add it to the recipient's mailbox
        // 3. Increment next_message_id
        // 4. Return the message ID
        todo!()
    }

    pub fn deliver_message(&mut self, actor: &mut dyn Actor) -> bool {
        // TODO: Deliver one message to the given actor
        // 1. Get the actor's mailbox
        // 2. Receive a message from the mailbox
        // 3. Call actor.receive() with the message
        // 4. Record the message in delivered_messages
        // 5. Return true if a message was delivered, false otherwise
        todo!()
    }

    pub fn run_until_idle(&mut self, actors: &mut HashMap<ActorId, Box<dyn Actor>>) {
        // TODO: Keep delivering messages until all mailboxes are empty
        // Process actors in round-robin fashion
        todo!()
    }

    pub fn has_pending_messages(&self, actor_id: ActorId) -> bool {
        self.mailboxes.get(&actor_id).map_or(false, |m| !m.is_empty())
    }

    pub fn get_delivered_messages(&self) -> &[Message] {
        &self.delivered_messages
    }
}

// Example actor implementations for testing
#[derive(Debug)]
pub struct EchoActor {
    id: ActorId,
    pub echo_count: usize,
}

impl EchoActor {
    pub fn new(id: ActorId) -> Self {
        Self { id, echo_count: 0 }
    }
}

impl Actor for EchoActor {
    fn id(&self) -> ActorId {
        self.id
    }

    fn receive(&mut self, message: Message, system: &mut ActorSystem) {
        // TODO: Echo the message back to the sender
        // Prepend "Echo: " to the content
        todo!()
    }
}

#[derive(Debug)]
pub struct CounterActor {
    id: ActorId,
    pub count: u32,
}

impl CounterActor {
    pub fn new(id: ActorId) -> Self {
        Self { id, count: 0 }
    }
}

impl Actor for CounterActor {
    fn id(&self) -> ActorId {
        self.id
    }

    fn receive(&mut self, message: Message, _system: &mut ActorSystem) {
        // TODO: Increment counter based on message content
        // If message content is "increment", increment count
        todo!()
    }
}

#[derive(Debug)]
pub struct ForwarderActor {
    id: ActorId,
    forward_to: ActorId,
}

impl ForwarderActor {
    pub fn new(id: ActorId, forward_to: ActorId) -> Self {
        Self { id, forward_to }
    }
}

impl Actor for ForwarderActor {
    fn id(&self) -> ActorId {
        self.id
    }

    fn receive(&mut self, message: Message, system: &mut ActorSystem) {
        // TODO: Forward the message to the designated actor
        // Append " (forwarded)" to the content
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_message_passing() {
        let mut system = ActorSystem::new();
        system.register_actor(1);
        system.register_actor(2);

        let msg_id = system.send_message(1, 2, "Hello".to_string());

        assert_eq!(msg_id, 0);
        assert!(system.has_pending_messages(2));
        assert!(!system.has_pending_messages(1));
    }

    #[test]
    fn test_echo_actor() {
        let mut system = ActorSystem::new();
        let mut actors: HashMap<ActorId, Box<dyn Actor>> = HashMap::new();

        let echo = Box::new(EchoActor::new(1));
        system.register_actor(1);
        system.register_actor(2);
        actors.insert(1, echo);

        system.send_message(2, 1, "Test".to_string());
        system.deliver_message(actors.get_mut(&1).unwrap().as_mut());

        // Should have sent echo back to actor 2
        assert!(system.has_pending_messages(2));
    }

    #[test]
    fn test_counter_actor() {
        let mut system = ActorSystem::new();
        system.register_actor(1);
        system.register_actor(2);

        let mut counter = CounterActor::new(1);

        system.send_message(2, 1, "increment".to_string());
        system.send_message(2, 1, "increment".to_string());
        system.send_message(2, 1, "increment".to_string());

        system.deliver_message(&mut counter);
        system.deliver_message(&mut counter);
        system.deliver_message(&mut counter);

        assert_eq!(counter.count, 3);
    }

    #[test]
    fn test_message_forwarding() {
        let mut system = ActorSystem::new();
        system.register_actor(1);
        system.register_actor(2);
        system.register_actor(3);

        let mut forwarder = ForwarderActor::new(2, 3);

        system.send_message(1, 2, "Forward this".to_string());
        system.deliver_message(&mut forwarder);

        // Should have forwarded to actor 3
        assert!(system.has_pending_messages(3));
    }

    #[test]
    fn test_multiple_messages_fifo() {
        let mut system = ActorSystem::new();
        system.register_actor(1);
        system.register_actor(2);

        system.send_message(1, 2, "First".to_string());
        system.send_message(1, 2, "Second".to_string());
        system.send_message(1, 2, "Third".to_string());

        let mut counter = CounterActor::new(2);

        system.deliver_message(&mut counter);
        let delivered = system.get_delivered_messages();
        assert_eq!(delivered[0].content, "First");

        system.deliver_message(&mut counter);
        let delivered = system.get_delivered_messages();
        assert_eq!(delivered[1].content, "Second");
    }

    #[test]
    fn test_run_until_idle() {
        let mut system = ActorSystem::new();
        let mut actors: HashMap<ActorId, Box<dyn Actor>> = HashMap::new();

        system.register_actor(1);
        system.register_actor(2);
        actors.insert(1, Box::new(CounterActor::new(1)));
        actors.insert(2, Box::new(CounterActor::new(2)));

        system.send_message(0, 1, "increment".to_string());
        system.send_message(0, 2, "increment".to_string());
        system.send_message(0, 1, "increment".to_string());

        system.run_until_idle(&mut actors);

        // All messages should be delivered
        assert!(!system.has_pending_messages(1));
        assert!(!system.has_pending_messages(2));
        assert_eq!(system.get_delivered_messages().len(), 3);
    }

    #[test]
    fn test_message_chain() {
        let mut system = ActorSystem::new();
        let mut actors: HashMap<ActorId, Box<dyn Actor>> = HashMap::new();

        system.register_actor(1);
        system.register_actor(2);
        system.register_actor(3);

        actors.insert(1, Box::new(ForwarderActor::new(1, 2)));
        actors.insert(2, Box::new(ForwarderActor::new(2, 3)));
        actors.insert(3, Box::new(CounterActor::new(3)));

        system.send_message(0, 1, "Start".to_string());
        system.run_until_idle(&mut actors);

        // Message should have been forwarded through the chain
        let delivered = system.get_delivered_messages();
        assert!(delivered.len() >= 3);
    }
}
