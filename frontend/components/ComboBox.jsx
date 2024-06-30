"use client"

import * as React from "react"
import { Button } from "@/components/Button"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/Command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/Popover"

const products = [
  { value: 'product1', label: 'Product 1' },
  { value: 'product2', label: 'Product 2' },
  { value: 'product3', label: 'Product 3' },
];

export function ComboboxDemo() {
  const [open, setOpen] = React.useState(false)
  const [value, setValue] = React.useState("")

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[200px] justify-between"
        >
          {value
            ? products.find((product) => product.value === value)?.label
            : "Select product..."}
          <span className="ml-2 h-4 w-4 shrink-0 opacity-50">▼</span> {/* Using a simple down arrow */}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search product..." className="h-9" />
          <CommandList>
            <CommandEmpty>No product found.</CommandEmpty>
            <CommandGroup>
              {products.map((product) => (
                <CommandItem
                  key={product.value}
                  value={product.value}
                  onSelect={(currentValue) => {
                    setValue(currentValue === value ? "" : currentValue)
                    setOpen(false)
                  }}
                >
                  {product.label}
                  <span
                    className={cn(
                      "ml-auto h-4 w-4",
                      value === product.value ? "opacity-100" : "opacity-0"
                    )}
                  >
                    ✓ {/* Using a simple check mark */}
                  </span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
export default ComboboxDemo;
