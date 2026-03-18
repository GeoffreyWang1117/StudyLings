// os09_reader_writer.rs
//
// The Reader-Writer problem involves synchronizing access to a shared resource where
// multiple readers can access the resource simultaneously, but writers need exclusive
// access. This is a fundamental concurrency control problem.
//
// Your task: Implement reader-writer locks with different fairness policies.

// I AM NOT DONE

use std::sync::{Arc, Condvar, Mutex};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LockPolicy {
    ReadersPreference,  // Readers are preferred, writers may starve
    WritersPreference,  // Writers are preferred, readers may starve
    Fair,               // Fair scheduling, no starvation
}

struct RwLockState {
    readers: usize,
    writers: usize,
    waiting_readers: usize,
    waiting_writers: usize,
}

pub struct RwLock<T> {
    data: Mutex<T>,
    state: Mutex<RwLockState>,
    read_condvar: Condvar,
    write_condvar: Condvar,
    policy: LockPolicy,
}

impl<T> RwLock<T> {
    pub fn new(data: T, policy: LockPolicy) -> Arc<Self> {
        // TODO: Create a new reader-writer lock with the given policy
        todo!()
    }

    pub fn read(&self) -> ReadGuard<T> {
        // TODO: Acquire a read lock
        // The behavior depends on the policy:
        // - ReadersPreference: Acquire if no writers
        // - WritersPreference: Acquire if no writers and no waiting writers
        // - Fair: Use a queue-like mechanism
        todo!()
    }

    pub fn write(&self) -> WriteGuard<T> {
        // TODO: Acquire a write lock
        // Must wait until no readers and no other writers
        todo!()
    }

    fn can_read(&self, state: &RwLockState) -> bool {
        // TODO: Determine if a reader can acquire the lock based on policy
        todo!()
    }

    fn can_write(&self, state: &RwLockState) -> bool {
        // TODO: Determine if a writer can acquire the lock
        // Writers need exclusive access (no readers, no other writers)
        todo!()
    }

    pub fn reader_count(&self) -> usize {
        let state = self.state.lock().unwrap();
        state.readers
    }

    pub fn writer_count(&self) -> usize {
        let state = self.state.lock().unwrap();
        state.writers
    }

    pub fn waiting_readers(&self) -> usize {
        let state = self.state.lock().unwrap();
        state.waiting_readers
    }

    pub fn waiting_writers(&self) -> usize {
        let state = self.state.lock().unwrap();
        state.waiting_writers
    }
}

pub struct ReadGuard<'a, T> {
    lock: &'a RwLock<T>,
    data: *const T,
}

impl<'a, T> ReadGuard<'a, T> {
    fn new(lock: &'a RwLock<T>) -> Self {
        // TODO: Create a read guard
        // This should increment the reader count
        todo!()
    }
}

impl<'a, T> Drop for ReadGuard<'a, T> {
    fn drop(&mut self) {
        // TODO: Release the read lock
        // Decrement reader count and notify waiting writers
        todo!()
    }
}

impl<'a, T> std::ops::Deref for ReadGuard<'a, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { &*self.data }
    }
}

pub struct WriteGuard<'a, T> {
    lock: &'a RwLock<T>,
    data: *mut T,
}

impl<'a, T> WriteGuard<'a, T> {
    fn new(lock: &'a RwLock<T>) -> Self {
        // TODO: Create a write guard
        // This should increment the writer count
        todo!()
    }
}

impl<'a, T> Drop for WriteGuard<'a, T> {
    fn drop(&mut self) {
        // TODO: Release the write lock
        // Decrement writer count and notify waiting readers/writers
        todo!()
    }
}

impl<'a, T> std::ops::Deref for WriteGuard<'a, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { &*self.data }
    }
}

impl<'a, T> std::ops::DerefMut for WriteGuard<'a, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        unsafe { &mut *self.data }
    }
}

// Safe wrappers that ensure Send + Sync
unsafe impl<T: Send> Send for RwLock<T> {}
unsafe impl<T: Send + Sync> Sync for RwLock<T> {}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    use std::time::Duration;

    #[test]
    fn test_single_reader() {
        let lock = RwLock::new(42, LockPolicy::Fair);
        let guard = lock.read();
        assert_eq!(*guard, 42);
    }

    #[test]
    fn test_single_writer() {
        let lock = RwLock::new(42, LockPolicy::Fair);
        let mut guard = lock.write();
        *guard = 100;
        assert_eq!(*guard, 100);
    }

    #[test]
    fn test_multiple_readers() {
        let lock = RwLock::new(0, LockPolicy::ReadersPreference);

        let mut handles = vec![];
        for _ in 0..5 {
            let lock_clone = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                let guard = lock_clone.read();
                thread::sleep(Duration::from_millis(10));
                *guard
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }
    }

    #[test]
    fn test_reader_writer_exclusion() {
        let lock = RwLock::new(0, LockPolicy::Fair);
        let lock_clone = Arc::clone(&lock);

        let writer = thread::spawn(move || {
            let mut guard = lock_clone.write();
            *guard = 1;
            thread::sleep(Duration::from_millis(50));
            *guard = 2;
        });

        thread::sleep(Duration::from_millis(10));

        let reader = thread::spawn(move || {
            let guard = lock.read();
            *guard
        });

        writer.join().unwrap();
        let value = reader.join().unwrap();

        // Reader should see the final value after writer completes
        assert_eq!(value, 2);
    }

    #[test]
    fn test_writers_preference() {
        let lock = RwLock::new(0, LockPolicy::WritersPreference);

        let guard = lock.read();
        assert_eq!(lock.reader_count(), 1);
        drop(guard);

        let mut guard = lock.write();
        *guard = 42;
        drop(guard);

        let guard = lock.read();
        assert_eq!(*guard, 42);
    }

    #[test]
    fn test_readers_preference() {
        let lock = RwLock::new(0, LockPolicy::ReadersPreference);
        let lock_clone = Arc::clone(&lock);

        let _reader1 = lock.read();

        let writer = thread::spawn(move || {
            thread::sleep(Duration::from_millis(20));
            let mut guard = lock_clone.write();
            *guard = 100;
        });

        thread::sleep(Duration::from_millis(10));

        // With readers preference, this reader should be able to acquire
        let _reader2 = lock.read();
        assert_eq!(lock.reader_count(), 2);

        drop(_reader1);
        drop(_reader2);

        writer.join().unwrap();
    }

    #[test]
    fn test_concurrent_readers() {
        let lock = RwLock::new(vec![1, 2, 3, 4, 5], LockPolicy::Fair);

        let mut handles = vec![];
        for _ in 0..10 {
            let lock_clone = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                let guard = lock_clone.read();
                let sum: i32 = guard.iter().sum();
                sum
            });
            handles.push(handle);
        }

        for handle in handles {
            let sum = handle.join().unwrap();
            assert_eq!(sum, 15);
        }
    }

    #[test]
    fn test_sequential_writers() {
        let lock = RwLock::new(0, LockPolicy::Fair);

        let mut handles = vec![];
        for i in 0..5 {
            let lock_clone = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                let mut guard = lock_clone.write();
                *guard += i;
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        let guard = lock.read();
        assert_eq!(*guard, 10); // 0 + 1 + 2 + 3 + 4
    }

    #[test]
    fn test_alternating_read_write() {
        let lock = RwLock::new(0, LockPolicy::Fair);

        for i in 0..10 {
            if i % 2 == 0 {
                let mut guard = lock.write();
                *guard += 1;
            } else {
                let guard = lock.read();
                assert!(*guard > 0);
            }
        }

        let guard = lock.read();
        assert_eq!(*guard, 5); // 5 writes
    }

    #[test]
    fn test_fair_policy() {
        let lock = RwLock::new(0, LockPolicy::Fair);
        let lock_clone = Arc::clone(&lock);

        // Hold read lock
        let reader = lock.read();

        // Writer waits
        let writer = thread::spawn(move || {
            thread::sleep(Duration::from_millis(10));
            let mut guard = lock_clone.write();
            *guard = 42;
        });

        thread::sleep(Duration::from_millis(20));
        drop(reader);

        writer.join().unwrap();

        let guard = lock.read();
        assert_eq!(*guard, 42);
    }

    #[test]
    fn test_no_writer_starvation() {
        let lock = RwLock::new(0, LockPolicy::WritersPreference);

        let mut handles = vec![];

        // Spawn a writer that should eventually execute
        let lock_writer = Arc::clone(&lock);
        let writer = thread::spawn(move || {
            thread::sleep(Duration::from_millis(10));
            let mut guard = lock_writer.write();
            *guard = 999;
        });

        // Spawn many readers
        for _ in 0..5 {
            let lock_reader = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                let guard = lock_reader.read();
                thread::sleep(Duration::from_millis(5));
                *guard
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        writer.join().unwrap();

        let guard = lock.read();
        assert_eq!(*guard, 999);
    }

    #[test]
    fn test_reader_count() {
        let lock = RwLock::new(42, LockPolicy::Fair);

        assert_eq!(lock.reader_count(), 0);

        let _g1 = lock.read();
        assert_eq!(lock.reader_count(), 1);

        let _g2 = lock.read();
        assert_eq!(lock.reader_count(), 2);

        drop(_g1);
        assert_eq!(lock.reader_count(), 1);

        drop(_g2);
        assert_eq!(lock.reader_count(), 0);
    }

    #[test]
    fn test_writer_count() {
        let lock = RwLock::new(42, LockPolicy::Fair);

        assert_eq!(lock.writer_count(), 0);

        let _guard = lock.write();
        assert_eq!(lock.writer_count(), 1);

        drop(_guard);
        assert_eq!(lock.writer_count(), 0);
    }

    #[test]
    fn test_stress_test() {
        let lock = RwLock::new(0, LockPolicy::Fair);
        let num_iterations = 100;

        let mut handles = vec![];

        // Spawn readers
        for _ in 0..10 {
            let lock_clone = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                for _ in 0..num_iterations {
                    let _guard = lock_clone.read();
                    thread::sleep(Duration::from_micros(10));
                }
            });
            handles.push(handle);
        }

        // Spawn writers
        for _ in 0..5 {
            let lock_clone = Arc::clone(&lock);
            let handle = thread::spawn(move || {
                for _ in 0..num_iterations {
                    let mut guard = lock_clone.write();
                    *guard += 1;
                    thread::sleep(Duration::from_micros(10));
                }
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        let guard = lock.read();
        assert_eq!(*guard, 500); // 5 writers * 100 iterations
    }
}
