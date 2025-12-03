import os
import re
from google.colab import drive

def universal_vocabulary_reader(file_path):
    """Read vocabulary from ANY format: PDF, DOCX, TXT, etc."""
    
    print(f"📖 READING FILE: {file_path}")
    print(f"📄 File type: {os.path.splitext(file_path)[1]}")
    
    try:
        # 1. PDF Files
        if file_path.lower().endswith('.pdf'):
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                print(f"✅ PDF read successfully: {len(text)} characters")
                return text
            except Exception as e:
                print(f"❌ PDF reading failed: {e}")
                return None
        
        # 2. Word Documents (.docx)
        elif file_path.lower().endswith('.docx'):
            try:
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                print(f"✅ DOCX read successfully: {len(text)} characters")
                return text
            except Exception as e:
                print(f"❌ DOCX reading failed: {e}")
                return None
        
        # 3. Plain Text Files (.txt)
        elif file_path.lower().endswith('.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                print(f"✅ TXT read successfully: {len(text)} characters")
                return text
            except Exception as e:
                print(f"❌ TXT reading failed: {e}")
                return None
        
        # 4. Other formats - try as text
        else:
            print(f"⚠️ Unknown format, trying as text file...")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                print(f"✅ File read as text: {len(text)} characters")
                return text
            except Exception as e:
                print(f"❌ Could not read file: {e}")
                return None
                
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def fix_multi_line_definitions(text):
    """Fix definitions that span multiple lines"""
    
    lines = text.split('\n')
    combined_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # If line starts with number or has arrow/colon/dash, it's a new entry
        if (line[0].isdigit() or 
            ' → ' in line or 
            ': ' in line or 
            ' - ' in line or
            '. ' in line):
            combined_lines.append(line)
        else:
            # This is a continuation of previous definition
            if combined_lines:
                combined_lines[-1] = combined_lines[-1] + " " + line
    
    return '\n'.join(combined_lines)

def process_vocabulary_text(text):
    """Your exact processing logic - unchanged"""
    
    print("🔍 PROCESSING VOCABULARY")
    print("=" * 60)

    # First fix multi-line issues
    text = fix_multi_line_definitions(text)
    
    # Split into lines
    lines = text.split('\n')
    print(f"📊 Total lines: {len(lines)}")

    # Find vocabulary lines
    vocabulary_lines = []
    for line in lines:
        line = line.strip()
        if line:
            # Keep lines that either start with number OR have separator
            if (line[0].isdigit() or 
                ' → ' in line or 
                ': ' in line or 
                ' - ' in line):
                vocabulary_lines.append(line)

    print(f"📝 Vocabulary lines found: {len(vocabulary_lines)}")

    # Process each line
    vocabulary_dict = {}
    all_entries = []

    for line in vocabulary_lines:
        try:
            original_num = 0
            word_part = ""
            definition = ""
            
            # Check for different separators
            if ' → ' in line:
                separator = ' → '
            elif ': ' in line:
                separator = ': '
            elif ' - ' in line:
                separator = ' - '
            else:
                separator = None
            
            if separator:
                # Handle numbered format: "1. Word → definition"
                if line[0].isdigit() and '. ' in line:
                    number_part, rest = line.split('. ', 1)
                    if number_part.strip().isdigit():
                        original_num = int(number_part)
                        if separator in rest:
                            word_part, definition = rest.split(separator, 1)
                else:
                    # Simple format: "Word → definition"
                    word_part, definition = line.split(separator, 1)
            
            if word_part and definition:
                word = word_part.strip()
                definition = definition.strip()
                
                # Clean word
                word = word.replace('"', '').replace("'", "").replace('!', '')
                
                # Store entry
                all_entries.append((original_num, word, definition))
                
                if word in vocabulary_dict:
                    vocabulary_dict[word].append((original_num, definition))
                else:
                    vocabulary_dict[word] = [(original_num, definition)]
                    
        except Exception as e:
            print(f"⚠️ Skipping line: {line[:50]}...")

    print(f"\n🎯 PROCESSING RESULTS:")
    print(f"   • Successfully processed: {len(all_entries)} entries")
    print(f"   • Unique words: {len(vocabulary_dict)}")

    # Find duplicates
    duplicates = {word: entries for word, entries in vocabulary_dict.items() if len(entries) > 1}

    print(f"\n🔄 DUPLICATE ANALYSIS:")
    print(f"   • Duplicate words: {len(duplicates)}")

    if duplicates:
        print(f"\n📋 DUPLICATE WORDS:")
        for word, entries in sorted(duplicates.items()):
            print(f"   • '{word}' appears {len(entries)} times:")
            for num, defn in entries:
                num_display = f"#{num}" if num > 0 else "no number"
                print(f"     {num_display}: {defn}")

    # Show the count math
    print(f"\n🧮 THE MATH EXPLAINED:")
    print(f"   Total entries: {len(all_entries)}")
    print(f"   Unique words: {len(vocabulary_dict)}")
    print(f"   Duplicates removed: {len(all_entries) - len(vocabulary_dict)}")

    # Sort all entries A-Z (keeping duplicates)
    print(f"\n📚 ALL {len(all_entries)} ENTRIES SORTED A-Z:")
    print("=" * 70)

    sorted_entries = sorted(all_entries, key=lambda x: x[1].lower())

    for i, (original_num, word, definition) in enumerate(sorted_entries, 1):
        is_duplicate = word in duplicates
        marker = " ⚠️" if is_duplicate else ""
        
        num_display = f"(was #{original_num})" if original_num > 0 else ""
        
        print(f"{i:3d}. {word:<25}{marker} → {definition}  {num_display}")

    print(f"\n✅ FINAL: {len(sorted_entries)} entries sorted A-Z")
    print(f"📊 Includes {len(duplicates)} duplicate words marked with ⚠️")
    
    return sorted_entries

def save_vocabulary(entries, output_file="vocabulary_sorted.txt"):
    """Save sorted vocabulary to file"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("VOCABULARY SORTED A-Z\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total entries: {len(entries)}\n\n")
        
        for i, (original_num, word, definition) in enumerate(entries, 1):
            num_display = f"(was #{original_num})" if original_num > 0 else ""
            f.write(f"{i:3d}. {word} → {definition} {num_display}\n")
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"📁 Full path: {os.path.abspath(output_file)}")

# 🚀 COMPLETE PIPELINE - USE THIS!
def extract_and_sort_vocabulary(file_path):
    """Complete pipeline: Read any format → Extract → Sort → Save"""
    
    print("🚀 UNIVERSAL VOCABULARY EXTRACTOR")
    print("=" * 60)
    
    # Step 1: Read file
    text = universal_vocabulary_reader(file_path)
    
    if not text:
        print("❌ Could not read file")
        return
    
    # Step 2: Show preview
    print(f"\n🔍 FILE PREVIEW (first 500 chars):")
    print("=" * 50)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("=" * 50)
    
    # Step 3: Process vocabulary
    sorted_entries = process_vocabulary_text(text)
    
    if sorted_entries:
        # Step 4: Save results
        output_file = f"vocabulary_{os.path.basename(file_path).split('.')[0]}_sorted.txt"
        save_vocabulary(sorted_entries, output_file)
        
        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"   • File: {file_path}")
        print(f"   • Format: {os.path.splitext(file_path)[1]}")
        print(f"   • Entries: {len(sorted_entries)}")
        print(f"   • Output: {output_file}")
    else:
        print("❌ No vocabulary found in file")

# 🎯 USE CASE:

# First mount Google Drive
drive.mount('/content/drive')

# Then specify your file path and run:
file_path = "/content/drive/My Drive/Documents/words3.pdf"  # Change to your file
extract_and_sort_vocabulary(file_path)

# Or for a Word document:
# file_path = "/content/drive/My Drive/Documents/words.docx"
# extract_and_sort_vocabulary(file_path)

# Or for a text file:
# file_path = "/content/drive/My Drive/Documents/words.txt"
# extract_and_sort_vocabulary(file_path)
