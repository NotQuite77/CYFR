import random

def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Clean the secret message (keep only uppercase letters)
        secret_clean = "".join([c.upper() for c in plaintext if c.isalpha()])
        if not secret_clean:
            return "Error: Message must contain letters for punctuation encoding."

        # 2. IMMENSE STEGANOGRAPHY DICTIONARY POOLS
        subjects = [
            "honestly my week", "the weekend", "that new place", "our original plan", 
            "the weather", "my current schedule", "everyone", "the whole group",
            "that casual coffee meetup", "the late-night group chat", "my morning routine",
            "the neighborhood vibe", "that random dinner idea", "the traffic situation",
            "our weekend road trip", "the backyard hangout", "my latest side project",
            "that documentary we talked about", "the vibe in the room", "my social battery",
            "the traffic downtown", "that local bakery", "my upcoming vacation", 
            "the new restaurant", "our old dynamic", "the conversation yesterday",
            "the project timeline", "the upcoming milestone", "the client feedback",
            "our team alignment", "the quarterly budget", "the sudden deadline shift",
            "the main presentation", "management's expectation", "the workflow automation",
            "our resource allocation", "the strategy bottleneck", "the final product release",
            "the team performance metric", "the project draft", "the shared calendar", 
            "the feedback loop", "our daily standup meeting", "the system upgrade",
            "the overall grand design", "every single moving part", "the creative momentum",
            "this entire collective journey", "the underlying cosmic rhythm", "my intuitive outlook",
            "our shared vision for the future", "the ongoing evolutionary shift", "this brief moment in time",
            "the bigger picture", "my general perspective", "the ultimate outcome"
        ]

        verbs = [
            "seems pretty busy", "turned out great", "looks really good", "is coming together", 
            "makes perfect sense", "feels a bit chaotic", "works for me", "is totally fine",
            "appears completely synchronized", "feels remarkably refreshing", "remains highly unpredictable",
            "sounds incredibly promising", "looks deceptively simple", "turned out to be a blessing",
            "feels slightly overwhelming", "looks very encouraging", "is completely manageable",
            "demands immediate attention", "requires an absolute overhaul", "drives the momentum forward",
            "accelerates our development", "complicates the entire pipeline", "simplifies the process tenfold",
            "solidifies our initial expectations", "disrupts the status quo", "harmonizes with our goals",
            "changes everything we planned", "requires a bit of patience", "creates a fresh opportunity",
            "drains my overall energy", "tests my absolute patience", "overwhelms the system entirely",
            "creates massive internal confusion", "sparks a bit of necessary tension", "soothes my anxiety",
            "stretches our limits to the maximum", "brings out the absolute best in us", "leaves much to be desired",
            "keeps everyone on their toes", "adds a layer of complexity", "inspires a lot of confidence"
        ]

        adjectives = [
            "for a change", "anyway", "to be fair", "right now", 
            "this time", "honestly", "overall", "lately",
            "unquestionably", "paradoxically", "without a doubt", "consequently",
            "coincidentally", "simultaneously", "theoretically", "practically",
            "essentially", "ultimately", "oddly enough", "interestingly",
            "all things considered", "frankly speaking", "ironically enough", "strictly speaking",
            "metaphorically looking", "unexpectedly", "systematically", "surprisingly",
            "especially these days", "typically", "undeniably", "fundamentally",
            "naturally", "as a matter of fact", "generally speaking", "for the time being"
        ]

        objects = [
            "with everything going on", "after a long day", "for the most part", 
            "if you think about it", "no matter what", "whenever you are free",
            "given the current global climate", "despite the technical limitations", "without any outside interference",
            "under these extreme circumstances", "behind closed doors", "in the grand scheme of things",
            "considering our current constraints", "all variations aside", "without skipping a beat",
            "within this short time constraint", "at this stage of the game", "regardless of the financial cost",
            "with the minimal resources we have left", "according to the latest internal data", "beyond our wildest expectations",
            "in the middle of this massive transition", "on a completely separate note", "in light of recent developments",
            "right at the critical moment", "based on what we know so far", "under the current infrastructure",
            "between you and me", "for those who care to notice", "across all structural operational levels",
            "deep within the core infrastructure", "with a touch of artistic flair", "under the radar",
            "with zero hidden expectations", "for anyone keeping track", "despite the initial pushback"
        ]

        connectors = [
            "so we should be good", "which is nice", "but we can adapt", "and I am glad", 
            "if that works", "so let me know", "which ultimately clears the air", "leaving no room for error",
            "so everything falls perfectly into place", "which is exactly what we needed to hear", "and it keeps us moving",
            "which solves our main issue", "so we are definitely on track", "and it brings us closer to finishing",
            "assuming nothing else breaks down", "even if it requires a backup plan", "but we must remain highly cautious",
            "which might cause a slight delay", "provided everyone agrees on the terms", "unless something changes drastically",
            "although it pushes our boundaries", "which forces us to look at it differently", "but it is worth the risk",
            "even though it takes more effort", "which introduces a slight gamble", "unless we decide to pivot completely",
            "so keep me updated on your progress", "which pretty much sums up my perspective", "and that is all that matters",
            "so we can cross that bridge when we get there", "which leaves the final decision up to you", "so let's make it happen",
            "so we can wrap this up shortly", "which gives us plenty of room to breathe", "and that completely makes sense"
        ]

        # Punctuation marks to scatter
        marks = [",", ".", ";", "!"]
        result_words = []

        # 3. Process each character in your secret message
        for char in secret_clean:
            # Convert letter to alphabet position (A=1, B=2, ..., Z=26)
            word_target = ord(char) - ord('A') + 1
            interval_words = []
            step = 0
            
            # 4. FIXED GRAMMAR LOOP: Keeps feeding words until the absolute math count is satisfied
            while len(interval_words) < word_target:
                pool_selector = step % 5
                if pool_selector == 0:
                    chosen_phrase = random.choice(subjects)
                elif pool_selector == 1:
                    chosen_phrase = random.choice(verbs)
                elif pool_selector == 2:
                    chosen_phrase = random.choice(adjectives)
                elif pool_selector == 3:
                    chosen_phrase = random.choice(objects)
                else:
                    chosen_phrase = random.choice(connectors)
                
                phrase_words = chosen_phrase.split()
                
                # Only add what is missing to prevent mid-phrase trailing breaks
                space_left = word_target - len(interval_words)
                if len(phrase_words) <= space_left:
                    interval_words.extend(phrase_words)
                else:
                    interval_words.extend(phrase_words[:space_left])
                step += 1

            result_words.extend(interval_words)
            
            # Slap a punctuation mark onto the last word of this group
            chosen_mark = random.choice(marks)
            result_words[-1] += chosen_mark

        # 6. Reconstruct a cleanly capitalized paragraph
        raw_paragraph = " ".join(result_words)
        
        sentences = []
        current_sentence = []
        for word in raw_paragraph.split():
            current_sentence.append(word)
            if word.endswith(('.', '!', ';')):
                sentences.append(" ".join(current_sentence).capitalize())
                current_sentence = []
        if current_sentence:
            sentences.append(" ".join(current_sentence).capitalize())
            
        final_output = " ".join(sentences)
        
        # Ensure the final string ends with a clean period instead of a loose comma
        if final_output[-1] in [',', ';']:
            final_output = final_output[:-1] + "."
        elif not final_output[-1].endswith(('.', '!')):
            final_output += "."
            
        return final_output
        
    except Exception as e:
        return f"Punctuation Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        raw_words = ciphertext.split()
        word_counter = 0
        secret_chars = []
        target_marks = (',', '.', ';', '!', '?')
        
        for word in raw_words:
            word_counter += 1
            
            if word.endswith(target_marks):
                ascii_val = word_counter + ord('A') - 1
                
                if ord('A') <= ascii_val <= ord('Z'):
                    secret_chars.append(chr(ascii_val))
                word_counter = 0
                
        if not secret_chars:
            return "Error: No punctuation intervals detected in this text."
            
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: Punctuation parsing failed ({str(e)})"