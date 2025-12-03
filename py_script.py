def process_vocabulary_text(vocabulary_text):
    """YOUR ORIGINAL CODE - Fixed to handle multi-line definitions"""
    
    print("🔍 PROCESSING VOCABULARY")
    print("=" * 60)

    # 🔧 FIX: First, combine lines that were split
    lines = vocabulary_text.split('\n')
    combined_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # If line starts with a number or has an arrow, it's a new entry
        if line[0].isdigit() or ' → ' in line:
            combined_lines.append(line)
        else:
            # This is a continuation of the previous definition
            # Append it to the last line
            if combined_lines:
                combined_lines[-1] = combined_lines[-1] + " " + line
    
    print(f"📊 After combining split lines: {len(combined_lines)} lines")

    # Now use the combined lines 
    vocabulary_lines = []
    for line in combined_lines:
        if line[0].isdigit() or ' → ' in line:
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
            
            if '. ' in line and ' → ' in line:
                if line[0].isdigit():
                    number_part, rest = line.split('. ', 1)
                    if number_part.strip().isdigit():
                        original_num = int(number_part)
                        word_part, definition = rest.split(' → ', 1)
                else:
                    word_part, definition = line.split(' → ', 1)
            elif ' → ' in line:
                word_part, definition = line.split(' → ', 1)
            
            if word_part and definition:
                word = word_part.strip()
                definition = definition.strip()
                
                word = word.replace('"', '').replace("'", "").replace('!', '')
                
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

# Test entry
test_text = """ """

print("🚀 TESTING MULTI-LINE DEFINITION FIX...")
process_vocabulary_text(test_text)
