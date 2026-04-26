import time
import pytest
from retry import retry


def test_retry_success_first_attempt():
    """Succès au premier essai"""
    call_count = 0
    
    @retry(max_attempts=3, base_delay=0.1)
    def succeed():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = succeed()
    assert result == "success"
    assert call_count == 1


def test_retry_succeeds_after_failures():
    """Succès après plusieurs tentatives"""
    call_count = 0
    
    @retry(max_attempts=3, base_delay=0.1)
    def fail_twice():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return "success"
    
    result = fail_twice()
    assert result == "success"
    assert call_count == 3


def test_retry_raises_after_max_attempts():
    """Lève l'exception après max_attempts"""
    call_count = 0
    
    @retry(max_attempts=3, base_delay=0.05)
    def always_fail():
        nonlocal call_count
        call_count += 1
        raise ValueError("persistent error")
    
    with pytest.raises(ValueError, match="persistent error"):
        always_fail()
    
    assert call_count == 3


def test_retry_exponential_backoff():
    """Vérifie le backoff exponentiel: delay = base_delay * 2^(attempt-1)"""
    call_count = 0
    times = []
    
    @retry(max_attempts=3, base_delay=0.1)
    def fail_twice():
        nonlocal call_count
        call_count += 1
        times.append(time.time())
        if call_count < 3:
            raise ValueError("fail")
        return "success"
    
    start = time.time()
    result = fail_twice()
    
    assert result == "success"
    assert len(times) == 3
    
    # Vérifier les délais (avec tolerance pour jitter et variabilité)
    # Entre attempt 1 et 2: delay ≈ 0.1 * 2^0 = 0.1
    delay1 = times[1] - times[0]
    # Entre attempt 2 et 3: delay ≈ 0.1 * 2^1 = 0.2
    delay2 = times[2] - times[1]
    
    assert 0.08 < delay1 < 0.15, f"Expected ~0.1s, got {delay1}"
    assert 0.18 < delay2 < 0.25, f"Expected ~0.2s, got {delay2}"


def test_retry_only_catches_specified_exceptions():
    """N'attrape que les exceptions spécifiées"""
    call_count = 0
    
    @retry(max_attempts=3, base_delay=0.05, exceptions=(ValueError,))
    def raise_key_error():
        nonlocal call_count
        call_count += 1
        raise KeyError("not caught")
    
    with pytest.raises(KeyError):
        raise_key_error()
    
    # Doit échouer au premier appel car KeyError n'est pas attrapée
    assert call_count == 1


def test_retry_catches_multiple_exception_types():
    """Attrape plusieurs types d'exceptions"""
    call_count = 0
    
    @retry(max_attempts=3, base_delay=0.05, exceptions=(ValueError, TypeError))
    def fail_with_type_error():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("first")
        elif call_count == 2:
            raise TypeError("second")
        return "success"
    
    result = fail_with_type_error()
    assert result == "success"
    assert call_count == 3


def test_retry_with_args_and_kwargs():
    """Fonctionne avec des arguments et des keyword arguments"""
    call_count = 0
    
    @retry(max_attempts=2, base_delay=0.05)
    def greet(name, greeting="Hello"):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("fail")
        return f"{greeting}, {name}"
    
    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice"
    assert call_count == 2


def test_retry_preserves_function_metadata():
    """Préserve les métadonnées de la fonction"""
    @retry(max_attempts=3, base_delay=0.1)
    def documented_function():
        """This is a documented function"""
        return "result"
    
    assert documented_function.__name__ == "documented_function"
    assert "documented function" in documented_function.__doc__
