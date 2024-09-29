key = "MATRIX"
plaintext = "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."

def create_matrix(key):
    """
    Створює матрицю 5x5 на основі ключа. Дублікати ключа видаляються, 'J' об'єднується з 'I'.
    """
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' і 'I' об'єднані
    key = ''.join(sorted(set(key), key=key.index))  # Видаляємо дублікати, зберігаючи порядок
    matrix_key = key + ''.join([c for c in alphabet if c not in key])
    
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(matrix_key[i:i+5])
    
    return matrix

def find_position(matrix, char):
    """
    Знаходить позицію символу в матриці (повертає рядок і стовпець).
    """
    for row in range(5):
        if char in matrix[row]:
            return row, matrix[row].index(char)
    return None

def preprocess_text(text):
    """
    Готує текст для шифрування: видаляє пробіли, об'єднує 'J' і 'I', розбиває на біграми.
    """
    text = text.upper().replace("J", "I").replace(" ", "")
    
    # Формуємо біграми
    bigrams = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] != text[i+1]:
            bigrams.append(text[i] + text[i+1])
            i += 2
        else:
            bigrams.append(text[i] + 'X')  # Якщо однакові літери або непарна кількість літер
            i += 1
    
    return bigrams

def encrypt(plaintext, key):
    """
    Шифрує текст за допомогою табличного шифру на основі фрази-ключа.
    """
    matrix = create_matrix(key)
    bigrams = preprocess_text(plaintext)
    
    ciphertext = ''
    for bigram in bigrams:
        row1, col1 = find_position(matrix, bigram[0])
        row2, col2 = find_position(matrix, bigram[1])
        
        if row1 == row2:
            # Якщо обидві літери в одному рядку
            ciphertext += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            # Якщо обидві літери в одному стовпці
            ciphertext += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            # Якщо утворюють прямокутник
            ciphertext += matrix[row1][col2] + matrix[row2][col1]
    
    return ciphertext

def decrypt(ciphertext, key):
    """
    Дешифрує текст за допомогою табличного шифру на основі фрази-ключа.
    """
    matrix = create_matrix(key)
    bigrams = preprocess_text(ciphertext)  # Прямий текст розбивається на біграми
    
    plaintext = ''
    for bigram in bigrams:
        row1, col1 = find_position(matrix, bigram[0])
        row2, col2 = find_position(matrix, bigram[1])
        
        if row1 == row2:
            # Якщо обидві літери в одному рядку
            plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            # Якщо обидві літери в одному стовпці
            plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            # Якщо утворюють прямокутник
            plaintext += matrix[row1][col2] + matrix[row2][col1]
    
    return plaintext

# Приклад використання
# Шифрування
ciphertext = encrypt(plaintext, key)
print(f"Зашифрований текст: {ciphertext}")

# Дешифрування
decrypted_text = decrypt(ciphertext, key)
print(f"Розшифрований текст: {decrypted_text}")
