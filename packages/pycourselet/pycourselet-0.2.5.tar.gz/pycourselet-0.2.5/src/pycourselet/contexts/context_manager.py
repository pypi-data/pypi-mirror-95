from typing import List, Optional, TypeVar, Type

from .context import Context

C = TypeVar('C', bound=Context)


class ContextManager:
    def __init__(self):
        self.base: List[Context] = list()
        self.stack: List[Context] = list()

    def current(self) -> Optional[Context]:
        return self.stack[-1] if self.stack else None

    def goto(self, context_type: Type[C]) -> Optional[C]:
        while len(self.stack) > 0:
            context = self.current()
            if type(context) is context_type:
                return context
            self.stack.pop()

        return None

    def exist_goto(self, context_type: Type[C]) -> bool:
        for item in self.stack:
            if type(item) is context_type:
                return True
        return False

    def create_branch(self, context_type: Type[C], **kwargs) -> C:
        context_type = context_type(**kwargs)
        self.base.append(context_type)

        self.stack.clear()
        self.stack.append(context_type)

        return context_type

    def push_create(self, context_type: Type[C], goto=True, **kwargs) -> C:
        needs = list()
        needs.append(context_type)

        need_settings = context_type.need()
        while need_settings:
            if goto:
                for sub_context in need_settings.contexts:
                    if self.exist_goto(sub_context):
                        self.goto(sub_context)

                        if need_settings.force_new:
                            self.stack.pop()
                            needs.append(need_settings.context)
                            break
            if type(self.current()) not in need_settings.contexts:
                needs.append(need_settings.context)
                need_settings = need_settings.context.need()
                continue
            break

        needs.reverse()
        for need_context in needs:
            context = need_context(**kwargs)
            self.push(context)

        return context

    def pop(self) -> Optional[Context]:
        return self.stack.pop()

    def push(self, context: Context) -> Context:
        current = self.current()
        if current:
            current.children.append(context)
            context.parent = current
        else:
            self.base.append(context)

        self.stack.append(context)

        return context
