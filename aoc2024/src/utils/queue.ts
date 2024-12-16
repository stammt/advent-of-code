type Element<T> = {
  value: T | null;
  next: Element<T> | null;
};

export class Queue<T> {
  head: Element<T> | null = null;
  //   tail: Element<T> | null = null;
  size: number = 0;

  hasNext(): boolean {
    return this.head !== null;
  }

  next(): T {
    const v = this.head!.value!;
    const tmp = this.head!;
    this.head = this.head!.next;

    // help the GC?
    tmp.next = null;
    tmp.value = null;

    this.size -= 1;
    return v;
  }

  prepend(value: T) {
    const e: Element<T> = { value: value, next: null };
    if (this.head !== null) {
      e.next = this.head;
    }
    this.head = e;
    this.size += 1;
  }

  //   append(value: T) {
  //     const e: Element<T> = { value: value, next: null };
  //     if (this.tail !== null) {
  //       this.tail.next = e;
  //     }
  //     this.tail = e;
  //     if (this.head === null) {
  //       this.head = e;
  //     }
  //     this.size += 1;
  //   }
}
