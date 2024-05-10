from blinker import Namespace

_entity_signals = Namespace()


register_entity = _entity_signals.signal('register_entity', """
                                            Signal emitted when a new entity is registered""")

update_entity = _entity_signals.signal('update_entity', """
                                            Signal emitted when an entity is updated""")

remove_entity = _entity_signals.signal('remove_entity', """
                                            Signal emitted when an entity is removed""")

get_entity = _entity_signals.signal('get_entity', """
                                            Signal emitted when an entity is retrieved""")      