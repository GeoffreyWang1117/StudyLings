// str10_text_similarity.rs
//
// Text Similarity Metrics
//
// Various algorithms to measure similarity between text documents.
// Useful for plagiarism detection, document clustering, recommendation systems.
//
// Time Complexity: Varies by algorithm (O(n) to O(n²))
// Space Complexity: Varies by algorithm (O(n) to O(n²))
//
// Key concepts:
// - Jaccard similarity: Set-based similarity (intersection / union)
// - Cosine similarity: Vector-based similarity using term frequencies
// - TF-IDF weighting: Term frequency × inverse document frequency
// - N-grams: Subsequences of n consecutive tokens
// - Used in search engines, plagiarism detection, clustering
//
// Your task: Implement multiple text similarity metrics.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

pub struct TextSimilarity;

impl TextSimilarity {
    pub fn jaccard_similarity(text1: &str, text2: &str) -> f64 {
        // TODO: Compute Jaccard similarity of word sets
        // - Convert texts to sets of words
        // - Jaccard = |intersection| / |union|
        // - Return value between 0.0 (no overlap) and 1.0 (identical)
        // - Handle empty sets (return 0.0)
        todo!()
    }

    pub fn jaccard_ngram_similarity(text1: &str, text2: &str, n: usize) -> f64 {
        // TODO: Compute Jaccard similarity of n-gram sets
        // - Generate n-grams (e.g., for n=2, "hello" -> ["he", "el", "ll", "lo"])
        // - Can be character n-grams or word n-grams
        // - Compute Jaccard similarity of n-gram sets
        todo!()
    }

    pub fn cosine_similarity(text1: &str, text2: &str) -> f64 {
        // TODO: Compute cosine similarity using term frequency vectors
        // - Build term frequency vectors for both texts
        // - Cosine = (v1 · v2) / (|v1| × |v2|)
        // - Dot product: sum of (freq1[term] × freq2[term]) for all terms
        // - Magnitude: sqrt(sum of freq²)
        // - Return value between 0.0 (orthogonal) and 1.0 (identical direction)
        todo!()
    }

    fn term_frequency(text: &str) -> HashMap<String, usize> {
        // TODO: Build term frequency map
        // - Split text into words (lowercase, trim punctuation)
        // - Count occurrences of each word
        // - Return HashMap of word -> count
        todo!()
    }

    fn dot_product(vec1: &HashMap<String, usize>, vec2: &HashMap<String, usize>) -> f64 {
        // TODO: Compute dot product of two term frequency vectors
        // - Sum of (vec1[term] × vec2[term]) for all common terms
        todo!()
    }

    fn magnitude(vec: &HashMap<String, usize>) -> f64 {
        // TODO: Compute magnitude (length) of term frequency vector
        // - sqrt(sum of freq²) for all terms
        todo!()
    }

    pub fn dice_coefficient(text1: &str, text2: &str) -> f64 {
        // TODO: Compute Dice coefficient (Sørensen-Dice)
        // - Dice = 2 × |intersection| / (|set1| + |set2|)
        // - Similar to Jaccard but weights intersection differently
        // - Return value between 0.0 and 1.0
        todo!()
    }

    pub fn overlap_coefficient(text1: &str, text2: &str) -> f64 {
        // TODO: Compute overlap coefficient (Szymkiewicz-Simpson)
        // - Overlap = |intersection| / min(|set1|, |set2|)
        // - Measures if smaller set is subset of larger
        // - Return value between 0.0 and 1.0
        todo!()
    }
}

pub struct TfidfSimilarity {
    documents: Vec<String>,
    idf: HashMap<String, f64>,
}

impl TfidfSimilarity {
    pub fn new(documents: Vec<String>) -> Self {
        let idf = Self::compute_idf(&documents);
        Self { documents, idf }
    }

    fn compute_idf(documents: &[String]) -> HashMap<String, f64> {
        // TODO: Compute IDF (Inverse Document Frequency) for all terms
        // - For each term, count how many documents contain it
        // - IDF(term) = log(total_documents / documents_containing_term)
        // - Higher IDF means term is more rare/distinctive
        todo!()
    }

    fn compute_tfidf(&self, text: &str) -> HashMap<String, f64> {
        // TODO: Compute TF-IDF vector for text
        // - TF-IDF(term) = TF(term) × IDF(term)
        // - TF can be raw count or normalized (count / total_terms)
        // - Return HashMap of term -> tf-idf score
        todo!()
    }

    pub fn similarity(&self, text1: &str, text2: &str) -> f64 {
        // TODO: Compute cosine similarity using TF-IDF vectors
        // - Compute TF-IDF vectors for both texts
        // - Use cosine similarity formula
        todo!()
    }

    pub fn most_similar(&self, query: &str) -> Option<(usize, f64)> {
        // TODO: Find most similar document to query
        // - Compute similarity between query and each document
        // - Return (document_index, similarity_score) of best match
        // - Return None if no documents
        todo!()
    }
}

pub struct NGramGenerator;

impl NGramGenerator {
    pub fn character_ngrams(text: &str, n: usize) -> Vec<String> {
        // TODO: Generate character n-grams
        // - Slide window of size n over text
        // - Example: "hello", n=2 -> ["he", "el", "ll", "lo"]
        todo!()
    }

    pub fn word_ngrams(text: &str, n: usize) -> Vec<String> {
        // TODO: Generate word n-grams
        // - Split into words, slide window of size n
        // - Example: "the quick brown fox", n=2 -> ["the quick", "quick brown", "brown fox"]
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jaccard_identical() {
        let similarity = TextSimilarity::jaccard_similarity("hello world", "hello world");
        assert_eq!(similarity, 1.0);
    }

    #[test]
    fn test_jaccard_disjoint() {
        let similarity = TextSimilarity::jaccard_similarity("abc def", "xyz uvw");
        assert_eq!(similarity, 0.0);
    }

    #[test]
    fn test_jaccard_partial() {
        let similarity = TextSimilarity::jaccard_similarity("the quick brown", "the lazy brown");
        // Intersection: {"the", "brown"} = 2
        // Union: {"the", "quick", "brown", "lazy"} = 4
        // Jaccard = 2/4 = 0.5
        assert_eq!(similarity, 0.5);
    }

    #[test]
    fn test_jaccard_ngram() {
        let similarity = TextSimilarity::jaccard_ngram_similarity("hello", "hallo", 2);
        // "hello": ["he", "el", "ll", "lo"]
        // "hallo": ["ha", "al", "ll", "lo"]
        // Intersection: {"ll", "lo"} = 2
        assert!(similarity > 0.0 && similarity < 1.0);
    }

    #[test]
    fn test_cosine_similarity_identical() {
        let similarity = TextSimilarity::cosine_similarity("hello world", "hello world");
        assert_eq!(similarity, 1.0);
    }

    #[test]
    fn test_cosine_similarity_different() {
        let similarity = TextSimilarity::cosine_similarity("cat dog", "bird fish");
        assert_eq!(similarity, 0.0);
    }

    #[test]
    fn test_cosine_similarity_partial() {
        let similarity = TextSimilarity::cosine_similarity(
            "the quick brown fox",
            "the lazy brown dog"
        );
        assert!(similarity > 0.0 && similarity < 1.0);
    }

    #[test]
    fn test_dice_coefficient() {
        let similarity = TextSimilarity::dice_coefficient("the quick brown", "the lazy brown");
        // Dice = 2 × 2 / (3 + 3) = 4/6 ≈ 0.667
        assert!(similarity > 0.6 && similarity < 0.7);
    }

    #[test]
    fn test_overlap_coefficient() {
        let similarity = TextSimilarity::overlap_coefficient("cat dog", "cat dog bird fish");
        // Overlap = 2 / min(2, 4) = 2/2 = 1.0
        assert_eq!(similarity, 1.0);
    }

    #[test]
    fn test_tfidf_similarity() {
        let documents = vec![
            "the quick brown fox".to_string(),
            "the lazy brown dog".to_string(),
            "the red fox".to_string(),
        ];

        let tfidf = TfidfSimilarity::new(documents);
        let sim = tfidf.similarity("the quick brown fox", "the lazy brown dog");

        assert!(sim > 0.0 && sim < 1.0);
    }

    #[test]
    fn test_tfidf_most_similar() {
        let documents = vec![
            "machine learning algorithms".to_string(),
            "deep learning neural networks".to_string(),
            "cooking recipes food".to_string(),
        ];

        let tfidf = TfidfSimilarity::new(documents);
        let result = tfidf.most_similar("artificial intelligence learning");

        assert!(result.is_some());
        let (idx, _) = result.unwrap();
        // Should match one of the learning-related documents (0 or 1)
        assert!(idx == 0 || idx == 1);
    }

    #[test]
    fn test_character_ngrams() {
        let ngrams = NGramGenerator::character_ngrams("hello", 2);
        assert_eq!(ngrams, vec!["he", "el", "ll", "lo"]);
    }

    #[test]
    fn test_word_ngrams() {
        let ngrams = NGramGenerator::word_ngrams("the quick brown fox", 2);
        assert_eq!(ngrams.len(), 3);
        assert!(ngrams.contains(&"the quick".to_string()));
        assert!(ngrams.contains(&"quick brown".to_string()));
        assert!(ngrams.contains(&"brown fox".to_string()));
    }

    #[test]
    fn test_empty_strings() {
        assert_eq!(TextSimilarity::jaccard_similarity("", ""), 0.0);
        assert_eq!(TextSimilarity::cosine_similarity("", "hello"), 0.0);
    }
}
