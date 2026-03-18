// mm02_raii.rs
//
// RAII (Resource Acquisition Is Initialization) is a programming idiom
// where resource lifetime is tied to object lifetime. Resources are
// acquired in constructor and released in destructor.
//
// Your task: Implement RAII wrappers for different resources.

// I AM NOT DONE

use std::collections::HashMap;

// Simulated file system
static mut FILE_SYSTEM: Option<HashMap<String, String>> = None;

fn init_fs() {
    unsafe {
        FILE_SYSTEM = Some(HashMap::new());
    }
}

fn write_file(path: &str, content: &str) {
    unsafe {
        if let Some(fs) = &mut FILE_SYSTEM {
            fs.insert(path.to_string(), content.to_string());
        }
    }
}

fn file_exists(path: &str) -> bool {
    unsafe {
        FILE_SYSTEM.as_ref()
            .map(|fs| fs.contains_key(path))
            .unwrap_or(false)
    }
}

fn delete_file(path: &str) {
    unsafe {
        if let Some(fs) = &mut FILE_SYSTEM {
            fs.remove(path);
        }
    }
}

pub struct FileHandle {
    path: String,
    closed: bool,
}

impl FileHandle {
    pub fn open(path: &str) -> Self {
        // TODO: Implement RAII file handle
        // Create file in simulated file system
        todo!()
    }

    pub fn write(&mut self, content: &str) -> Result<(), &'static str> {
        // TODO: Write to file if not closed
        todo!()
    }

    pub fn close(&mut self) {
        // TODO: Mark as closed (cleanup will happen in Drop)
        todo!()
    }

    pub fn is_closed(&self) -> bool {
        self.closed
    }
}

impl Drop for FileHandle {
    fn drop(&mut self) {
        // TODO: Implement automatic cleanup
        // Delete file from simulated file system
        todo!()
    }
}

// Lock implementation
static mut LOCK_STATE: bool = false;

pub struct Lock {
    acquired: bool,
}

impl Lock {
    pub fn acquire() -> Result<Self, &'static str> {
        // TODO: Acquire lock using RAII
        // Check if lock is available, acquire it
        todo!()
    }
}

impl Drop for Lock {
    fn drop(&mut self) {
        // TODO: Automatically release lock
        todo!()
    }
}

fn is_locked() -> bool {
    unsafe { LOCK_STATE }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_file_handle_raii() {
        init_fs();

        {
            let mut file = FileHandle::open("test.txt");
            file.write("hello").unwrap();
            assert!(file_exists("test.txt"));
        } // file should be deleted when dropped

        assert!(!file_exists("test.txt"));
    }

    #[test]
    fn test_explicit_close() {
        init_fs();

        let mut file = FileHandle::open("test.txt");
        file.close();
        assert!(file.is_closed());
        assert!(file.write("data").is_err());
    }

    #[test]
    fn test_lock_raii() {
        {
            let _lock = Lock::acquire().unwrap();
            assert!(is_locked());
            assert!(Lock::acquire().is_err()); // Can't acquire twice
        } // lock released

        assert!(!is_locked());
        assert!(Lock::acquire().is_ok()); // Can acquire again
    }
}
