// db11_inverted_index.rs
//
// Inverted Index is a data structure used in full-text search engines to map
// content (words) to their locations in documents. It's the fundamental structure
// behind search engines like Elasticsearch, Solr, and Lucene.
//
// Structure:
// - Term → List of documents containing the term
// - Each document entry can include position information
// - Supports efficient text search queries
//
// Operations:
// - Index documents (tokenize and build inverted lists)
// - Search for terms (find documents containing terms)
// - Boolean queries (AND, OR, NOT)
// - Phrase queries (words in sequence)
//
// Your task: Implement an inverted index with basic search capabilities.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

pub type DocumentId = usize;

#[derive(Debug, Clone)]
pub struct Posting {
    doc_id: DocumentId,
    positions: Vec<usize>, // Positions of the term in the document
}

pub struct InvertedIndex {
    index: HashMap<String, Vec<Posting>>,
    documents: HashMap<DocumentId, String>,
    next_doc_id: DocumentId,
}

impl InvertedIndex {
    pub fn new() -> Self {
        Self {
            index: HashMap::new(),
            documents: HashMap::new(),
            next_doc_id: 0,
        }
    }

    pub fn add_document(&mut self, text: &str) -> DocumentId {
        // TODO: Add a document to the index
        // Tokenize the text into words
        // For each word, record the document ID and positions
        // Store the document text
        // Return the assigned document ID
        todo!()
    }

    pub fn search(&self, term: &str) -> Vec<DocumentId> {
        // TODO: Search for documents containing the term
        // Look up the term in the index
        // Return list of document IDs containing the term
        todo!()
    }

    pub fn search_and(&self, terms: &[&str]) -> Vec<DocumentId> {
        // TODO: Search for documents containing ALL terms (AND query)
        // Find intersection of document lists for all terms
        // Return documents that contain all terms
        todo!()
    }

    pub fn search_or(&self, terms: &[&str]) -> Vec<DocumentId> {
        // TODO: Search for documents containing ANY term (OR query)
        // Find union of document lists for all terms
        // Return documents that contain at least one term
        todo!()
    }

    pub fn search_not(&self, include: &str, exclude: &str) -> Vec<DocumentId> {
        // TODO: Search for documents containing include but not exclude
        // Find documents with include term
        // Remove documents that also contain exclude term
        todo!()
    }

    pub fn search_phrase(&self, phrase: &str) -> Vec<DocumentId> {
        // TODO: Search for exact phrase (words in sequence)
        // Tokenize the phrase
        // Find documents containing all words
        // Check if words appear in consecutive positions
        todo!()
    }

    pub fn get_document(&self, doc_id: DocumentId) -> Option<&String> {
        self.documents.get(&doc_id)
    }

    fn tokenize(&self, text: &str) -> Vec<String> {
        // TODO: Tokenize text into words
        // Convert to lowercase
        // Split on whitespace and punctuation
        // Remove empty strings
        text.to_lowercase()
            .split_whitespace()
            .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()))
            .filter(|s| !s.is_empty())
            .map(String::from)
            .collect()
    }

    pub fn num_documents(&self) -> usize {
        self.documents.len()
    }

    pub fn num_terms(&self) -> usize {
        self.index.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_index() {
        let index = InvertedIndex::new();
        assert_eq!(index.num_documents(), 0);
        assert_eq!(index.num_terms(), 0);
    }

    #[test]
    fn test_add_document() {
        let mut index = InvertedIndex::new();
        let doc_id = index.add_document("hello world");

        assert_eq!(index.num_documents(), 1);
        assert_eq!(index.get_document(doc_id), Some(&"hello world".to_string()));
    }

    #[test]
    fn test_simple_search() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("hello world");
        let doc2 = index.add_document("hello rust");

        let results = index.search("hello");
        assert_eq!(results.len(), 2);
        assert!(results.contains(&doc1));
        assert!(results.contains(&doc2));

        let results = index.search("world");
        assert_eq!(results.len(), 1);
        assert!(results.contains(&doc1));
    }

    #[test]
    fn test_search_and() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("hello world");
        let doc2 = index.add_document("hello rust");
        let doc3 = index.add_document("world of rust");

        let results = index.search_and(&["hello", "world"]);
        assert_eq!(results.len(), 1);
        assert!(results.contains(&doc1));

        let results = index.search_and(&["hello", "rust"]);
        assert_eq!(results.len(), 1);
        assert!(results.contains(&doc2));
    }

    #[test]
    fn test_search_or() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("hello world");
        let doc2 = index.add_document("hello rust");
        let doc3 = index.add_document("goodbye world");

        let results = index.search_or(&["hello", "goodbye"]);
        assert_eq!(results.len(), 3);
    }

    #[test]
    fn test_search_not() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("hello world");
        let doc2 = index.add_document("hello rust");
        let doc3 = index.add_document("world of rust");

        let results = index.search_not("hello", "rust");
        assert_eq!(results.len(), 1);
        assert!(results.contains(&doc1));
    }

    #[test]
    fn test_search_phrase() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("hello world");
        let doc2 = index.add_document("world hello");
        let doc3 = index.add_document("hello beautiful world");

        let results = index.search_phrase("hello world");
        assert!(results.contains(&doc1));
        assert!(!results.contains(&doc2)); // Wrong order
    }

    #[test]
    fn test_case_insensitive_search() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("Hello World");
        let doc2 = index.add_document("HELLO WORLD");

        let results = index.search("hello");
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_multiple_occurrences() {
        let mut index = InvertedIndex::new();
        let doc_id = index.add_document("hello hello world");

        let results = index.search("hello");
        assert_eq!(results.len(), 1);
        assert!(results.contains(&doc_id));
    }

    #[test]
    fn test_empty_search() {
        let mut index = InvertedIndex::new();
        index.add_document("hello world");

        let results = index.search("nonexistent");
        assert_eq!(results.len(), 0);
    }

    #[test]
    fn test_punctuation_handling() {
        let mut index = InvertedIndex::new();
        let doc_id = index.add_document("Hello, world! How are you?");

        let results = index.search("hello");
        assert!(results.contains(&doc_id));

        let results = index.search("world");
        assert!(results.contains(&doc_id));
    }

    #[test]
    fn test_large_corpus() {
        let mut index = InvertedIndex::new();

        for i in 0..100 {
            index.add_document(&format!("document {} with content", i));
        }

        let results = index.search("document");
        assert_eq!(results.len(), 100);

        let results = index.search("content");
        assert_eq!(results.len(), 100);
    }

    #[test]
    fn test_complex_phrase_search() {
        let mut index = InvertedIndex::new();
        let doc1 = index.add_document("the quick brown fox jumps");
        let doc2 = index.add_document("quick brown fox");
        let doc3 = index.add_document("the brown quick fox");

        let results = index.search_phrase("quick brown fox");
        assert!(results.contains(&doc1));
        assert!(results.contains(&doc2));
        assert!(!results.contains(&doc3)); // Words not in order
    }
}
