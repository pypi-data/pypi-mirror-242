# sdlib: Stable Diffusion Library

*Example plugin that appends `", gloomy atmosphere"` to any positive prompt.*

```python
import sdlib
plugin = sdlib.register_plugin("my-plugin")

@plugin.wrapper
def encode_prompt_schedule(params: sdlib.EncodePromptScheduleParams, original_function):
    if params.is_positive:
        if params.prompt.strip():
            params.prompt += ", "
        params.prompt += "gloomy atmosphere"
    return original_function(params)
```

sdlib is a library that exposes many different components of the [Stable Diffusion Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) through a stable programming interface.
It takes care of much of the boilerplate so that extension developers can focus on writing useful code.

## Motivation

Developing extensions for the webui is currently very error-prone.
Monkey patching is commonplace, extensions break all the time shortly after a release.
There are many extension repositories that are stale because they are updated less often than the webui.

sdlib intends to help stabilize the interface extension developers program against so that things stop breaking all the time.

## Documentation

This guide provides basic documentation for plugins intercommunication.

### TL;DR:

1. Create a plugin using `plugin = sdlib.create_plugin("plugin_name", "0.0.1")`
2. Define a function and register it to a plugin using the `@plugin.function` decorator.
3. Use the `@plugin.wrapper` decorator to register a function wrapper. You can use the optional `after=` parameter to specify execution order.

### Create a plugin

Any change in the plugin system (registering a new function, wrapping a function, etc.) must be done through a plugin.

Here's how to declare a plugin:

```python
import sdlib
plugin = sdlib.register_plugin("my_awesome_plugin", api_version="0.0.1")
```

A plugin identifier is a series of underscores or lowercase letters (`[a-z_]+`).
The identifier of a plugin must be unique; two plugins cannot have the same identifier at the same time.

The version of a plugin is used to make sure the programming interface the code is written against stays consistent over time.

### Defining a Function

A function in sdlib is a regular Python function that can be registered to a plugin.
It performs a specific task and can be extended using wrappers.

#### Example:

```python
@plugin.function
def eat(food):
    return f"I eat {food}!"
```

### Using the `wrapper` Decorator

The `wrapper` decorator is used to extend or modify the behavior of a registered function.
The wrapper function must have the same name as the target function, unless the `name` parameter is used.

#### Without Parameters:

```python
@plugin.wrapper
def eat(food, original_function):
    return original_function(food).upper()
```

In this example, `eat` is a wrapper that converts the eating message to uppercase, extending the original `eat` function defined earlier.

#### With Parameters:

```python
@plugin.wrapper(name="eat", after="another_plugin")
def custom_eating(food, original_function):
    return f"{original_function(food)} You should as well!"
```

In this example, `custom_eating` adds an additional message to the original one.
The parameters of the annotation tells the plugin system to:

- wrap the `eat` function defined earlier instead of targeting an unknown entity named `"custom_eating"`
- only wrap after any wraps provided by `another_plugin`

### Applying Wrappers

Wrappers are applied in the order they are defined, unless specified otherwise using the `after` parameter.

### Using Generator Functions as Wrappers

Generator functions can also be used for wrappers.
In a generator wrapper, each `yield` statement calls the original function and receives its result.

Here’s how you can convert a regular function wrapper to a generator wrapper:

#### Regular Function Wrapper:

```python
@plugin.wrapper
def eat(food, original_function):
    return original_function(food).upper()
```

#### Generator Function Wrapper:

```python
@plugin.wrapper
def eat(food):
    result = yield food
    return result.upper()
```

In this generator wrapper example, the `eat` function yields the `food` to the original function and then receives the original function’s result.
The wrapper then proceeds to modify the result by converting it to uppercase before returning it.

You can also use multiple `yield` statements in a generator wrapper, which allows for more intricate interactions with the original function.
Each `yield` results in a call to the original function, and the generator receives the result of that call.

#### Example with Multiple Yields:
```python
@plugin.wrapper
def eat(food):
    result1 = yield food
    result2 = yield f"{result1} and it's delicious"
    return result2
```

In this example, the `eat` function calls the original function twice, first with the original `food` argument, and then with an additional question.
The final result is derived from the second call to the original function.

### Best Practices

- Make sure the parameter types of your wrappers match the original function definition.
- Use descriptive names for your functions and wrappers.
- When applicable, ensure that your wrapper does not accidentally override or disrupt the behavior of the original function.

## Contributing

Contributions are welcome.
