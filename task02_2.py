import math

key1 = "SECRET"
key2 = "CRYPTO"
plaintext = "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."


def create_permutation(key):
    """
    Створює перестановку на основі ключа, де кожна літера отримує індекс у порядку її появи.
    """
    sorted_key = sorted(list(key))
    permutation = []
    
    for char in key:
        permutation.append(sorted_key.index(char))
        sorted_key[sorted_key.index(char)] = None  # Уникання дублікатів
    
    return permutation

def encrypt_single(plaintext, key):
    """
    Шифрування тексту за допомогою простої перестановки на основі ключа.
    """
    key_length = len(key)
    permutation = create_permutation(key)

    # Доповнення тексту пробілами, щоб його довжина була кратною довжині ключа
    while len(plaintext) % key_length != 0:
        plaintext += ' '

    # Розбиваємо текст на блоки, кожен з яких відповідає одній рядку таблиці
    n_rows = math.ceil(len(plaintext) / key_length)
    table = [plaintext[i:i + key_length] for i in range(0, len(plaintext), key_length)]

    # Шифрування: беремо стовпці згідно з порядком перестановки
    ciphertext = ''
    for i in sorted(range(key_length), key=lambda x: permutation[x]):
        for row in table:
            ciphertext += row[i]
    
    return ciphertext

def decrypt_single(ciphertext, key):
    """
    Дешифрування тексту за допомогою простої перестановки на основі ключа.
    """
    key_length = len(key)
    permutation = create_permutation(key)
    
    n_rows = math.ceil(len(ciphertext) / key_length)
    
    # Створюємо порожню таблицю
    table = [''] * n_rows
    
    # Читаємо шифротекст по стовпцях у правильному порядку
    index = 0
    for i in sorted(range(key_length), key=lambda x: permutation[x]):
        for row in range(n_rows):
            if index < len(ciphertext):
                table[row] += ciphertext[index]
                index += 1
    
    # Дешифруємо, читаючи рядки
    plaintext = ''.join(table).rstrip()  # Видаляємо додаткові пробіли, якщо вони є
    
    return plaintext

def encrypt_double(plaintext, key1, key2):
    """
    Шифрування тексту за допомогою подвійної перестановки з двома ключами.
    """
    # Перша перестановка
    intermediate_text = encrypt_single(plaintext, key1)
    
    # Друга перестановка
    ciphertext = encrypt_single(intermediate_text, key2)
    
    return ciphertext

def decrypt_double(ciphertext, key1, key2):
    """
    Дешифрування тексту за допомогою подвійної перестановки з двома ключами.
    """
    # Зворотня друга перестановка
    intermediate_text = decrypt_single(ciphertext, key2)
    
    # Зворотня перша перестановка
    plaintext = decrypt_single(intermediate_text, key1)
    
    return plaintext

# Приклад використання
# Шифрування
ciphertext = encrypt_double(plaintext, key1, key2)
print(f"Зашифрований текст: {ciphertext}")

# Дешифрування
decrypted_text = decrypt_double(ciphertext, key1, key2)
print(f"Розшифрований текст: {decrypted_text}")
