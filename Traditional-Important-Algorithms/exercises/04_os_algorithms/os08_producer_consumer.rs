// os08_producer_consumer.rs
//
// The Producer-Consumer problem is a classic synchronization problem where producers
// generate data and place it in a buffer, while consumers remove data from the buffer.
// The challenge is to ensure that producers don't add data to a full buffer and
// consumers don't remove data from an empty buffer.
//
// Your task: Implement a thread-safe bounded buffer for the producer-consumer problem.

// I AM NOT DONE

use std::sync::{Arc, Condvar, Mutex};
use std::collections::VecDeque;

pub struct BoundedBuffer<T> {
    buffer: Mutex<VecDeque<T>>,
    not_empty: Condvar,
    not_full: Condvar,
    capacity: usize,
}

impl<T> BoundedBuffer<T> {
    pub fn new(capacity: usize) -> Arc<Self> {
        // TODO: Create a new bounded buffer with the given capacity
        todo!()
    }

    pub fn produce(&self, item: T) {
        // TODO: Add an item to the buffer
        // 1. Lock the buffer
        // 2. Wait while buffer is full (use not_full condvar)
        // 3. Add item to buffer
        // 4. Notify waiting consumers (use not_empty condvar)
        todo!()
    }

    pub fn consume(&self) -> T {
        // TODO: Remove and return an item from the buffer
        // 1. Lock the buffer
        // 2. Wait while buffer is empty (use not_empty condvar)
        // 3. Remove item from buffer
        // 4. Notify waiting producers (use not_full condvar)
        todo!()
    }

    pub fn try_produce(&self, item: T) -> Result<(), T> {
        // TODO: Try to add an item without blocking
        // Return Err(item) if buffer is full
        todo!()
    }

    pub fn try_consume(&self) -> Option<T> {
        // TODO: Try to remove an item without blocking
        // Return None if buffer is empty
        todo!()
    }

    pub fn len(&self) -> usize {
        // TODO: Return current number of items in buffer
        todo!()
    }

    pub fn is_empty(&self) -> bool {
        // TODO: Check if buffer is empty
        todo!()
    }

    pub fn is_full(&self) -> bool {
        // TODO: Check if buffer is full
        todo!()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }
}

// Multi-producer, multi-consumer queue
pub struct MPMCQueue<T> {
    buffer: Arc<BoundedBuffer<T>>,
}

impl<T> MPMCQueue<T> {
    pub fn new(capacity: usize) -> Self {
        Self {
            buffer: BoundedBuffer::new(capacity),
        }
    }

    pub fn send(&self, item: T) {
        self.buffer.produce(item);
    }

    pub fn recv(&self) -> T {
        self.buffer.consume()
    }

    pub fn try_send(&self, item: T) -> Result<(), T> {
        self.buffer.try_produce(item)
    }

    pub fn try_recv(&self) -> Option<T> {
        self.buffer.try_consume()
    }

    pub fn len(&self) -> usize {
        self.buffer.len()
    }

    pub fn is_empty(&self) -> bool {
        self.buffer.is_empty()
    }

    pub fn get_buffer(&self) -> Arc<BoundedBuffer<T>> {
        Arc::clone(&self.buffer)
    }
}

impl<T> Clone for MPMCQueue<T> {
    fn clone(&self) -> Self {
        Self {
            buffer: Arc::clone(&self.buffer),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_basic_produce_consume() {
        let buffer = BoundedBuffer::new(5);

        buffer.produce(1);
        buffer.produce(2);
        buffer.produce(3);

        assert_eq!(buffer.consume(), 1);
        assert_eq!(buffer.consume(), 2);
        assert_eq!(buffer.consume(), 3);
    }

    #[test]
    fn test_fifo_order() {
        let buffer = BoundedBuffer::new(3);

        buffer.produce("first");
        buffer.produce("second");
        buffer.produce("third");

        assert_eq!(buffer.consume(), "first");
        assert_eq!(buffer.consume(), "second");
        assert_eq!(buffer.consume(), "third");
    }

    #[test]
    fn test_buffer_capacity() {
        let buffer = BoundedBuffer::new(2);

        buffer.produce(1);
        buffer.produce(2);

        assert_eq!(buffer.len(), 2);
        assert!(buffer.is_full());
    }

    #[test]
    fn test_try_produce_full() {
        let buffer = BoundedBuffer::new(1);

        assert!(buffer.try_produce(1).is_ok());
        assert!(buffer.try_produce(2).is_err());
    }

    #[test]
    fn test_try_consume_empty() {
        let buffer: BoundedBuffer<i32> = BoundedBuffer::new(5);

        assert!(buffer.is_empty());
        assert_eq!(buffer.try_consume(), None);
    }

    #[test]
    fn test_single_producer_single_consumer() {
        let buffer = BoundedBuffer::new(10);
        let buffer_clone = Arc::clone(&buffer);

        let producer = thread::spawn(move || {
            for i in 0..20 {
                buffer_clone.produce(i);
            }
        });

        let consumer = thread::spawn(move || {
            let mut sum = 0;
            for _ in 0..20 {
                sum += buffer.consume();
            }
            sum
        });

        producer.join().unwrap();
        let sum = consumer.join().unwrap();

        assert_eq!(sum, 190); // Sum of 0..20
    }

    #[test]
    fn test_multiple_producers() {
        let buffer = BoundedBuffer::new(50);

        let mut producers = vec![];
        for i in 0..3 {
            let buffer_clone = Arc::clone(&buffer);
            let handle = thread::spawn(move || {
                for j in 0..10 {
                    buffer_clone.produce(i * 10 + j);
                }
            });
            producers.push(handle);
        }

        for handle in producers {
            handle.join().unwrap();
        }

        assert_eq!(buffer.len(), 30);
    }

    #[test]
    fn test_multiple_consumers() {
        let buffer = BoundedBuffer::new(50);

        // Fill buffer
        for i in 0..30 {
            buffer.produce(i);
        }

        let mut consumers = vec![];
        for _ in 0..3 {
            let buffer_clone = Arc::clone(&buffer);
            let handle = thread::spawn(move || {
                let mut local_sum = 0;
                for _ in 0..10 {
                    local_sum += buffer_clone.consume();
                }
                local_sum
            });
            consumers.push(handle);
        }

        let mut total_sum = 0;
        for handle in consumers {
            total_sum += handle.join().unwrap();
        }

        assert_eq!(total_sum, 435); // Sum of 0..30
    }

    #[test]
    fn test_mpmc_queue() {
        let queue = MPMCQueue::new(10);

        queue.send(1);
        queue.send(2);
        queue.send(3);

        assert_eq!(queue.recv(), 1);
        assert_eq!(queue.recv(), 2);
        assert_eq!(queue.recv(), 3);
    }

    #[test]
    fn test_mpmc_concurrent() {
        let queue = MPMCQueue::new(20);

        let mut handles = vec![];

        // Spawn producers
        for i in 0..3 {
            let q = queue.clone();
            let handle = thread::spawn(move || {
                for j in 0..10 {
                    q.send(i * 100 + j);
                    thread::sleep(Duration::from_micros(10));
                }
            });
            handles.push(handle);
        }

        // Spawn consumers
        for _ in 0..3 {
            let q = queue.clone();
            let handle = thread::spawn(move || {
                let mut count = 0;
                for _ in 0..10 {
                    q.recv();
                    count += 1;
                    thread::sleep(Duration::from_micros(10));
                }
                count
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        assert!(queue.is_empty());
    }

    #[test]
    fn test_producer_blocks_on_full() {
        let buffer = BoundedBuffer::new(2);

        buffer.produce(1);
        buffer.produce(2);

        let buffer_clone = Arc::clone(&buffer);
        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(50));
            buffer_clone.consume();
        });

        // This should block until consumer removes an item
        buffer.produce(3);

        handle.join().unwrap();
        assert!(buffer.len() <= 2);
    }

    #[test]
    fn test_consumer_blocks_on_empty() {
        let buffer = BoundedBuffer::new(5);

        let buffer_clone = Arc::clone(&buffer);
        let handle = thread::spawn(move || {
            thread::sleep(Duration::from_millis(50));
            buffer_clone.produce(42);
        });

        // This should block until producer adds an item
        let value = buffer.consume();

        handle.join().unwrap();
        assert_eq!(value, 42);
    }

    #[test]
    fn test_stress_test() {
        let buffer = BoundedBuffer::new(10);
        let num_items = 1000;

        let buffer_producer = Arc::clone(&buffer);
        let producer = thread::spawn(move || {
            for i in 0..num_items {
                buffer_producer.produce(i);
            }
        });

        let buffer_consumer = Arc::clone(&buffer);
        let consumer = thread::spawn(move || {
            let mut sum = 0;
            for _ in 0..num_items {
                sum += buffer_consumer.consume();
            }
            sum
        });

        producer.join().unwrap();
        let sum = consumer.join().unwrap();

        let expected = (0..num_items).sum();
        assert_eq!(sum, expected);
    }
}
