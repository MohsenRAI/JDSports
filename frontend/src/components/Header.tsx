import { Search, User, Heart, ShoppingBag, Mic } from "lucide-react"
import { Input } from "@/components/ui/input"

export default function Header() {
  return (
    <header className="bg-white">
      {/* Top status bar */}
      <div className="bg-gray-50 py-1 px-4 text-xs text-gray-600 text-right">
        <div className="flex items-center justify-end gap-4">
          <span>🔋 STATUS</span>
          <span>Find Store</span>
          <span>JD Blog</span>
          <span>Help</span>
          <span>We deliver to... 🇺🇸</span>
        </div>
      </div>

      {/* Main header */}
      <div className="px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <div className="text-black font-bold text-2xl">
              JD
              <div className="text-xs font-normal -mt-1">
                UNDISPUTED<br />
                KING OF TRAINERS
              </div>
            </div>
          </div>

          {/* Search bar */}
          <div className="flex-1 max-w-md mx-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                type="text"
                placeholder="Search Nike, adidas, new arrivals etc.?"
                className="pl-10 pr-10 py-2 w-full"
              />
              <Mic className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            </div>
          </div>

          {/* Right icons */}
          <div className="flex items-center gap-4">
            <User className="h-5 w-5 text-gray-700 cursor-pointer" />
            <Heart className="h-5 w-5 text-gray-700 cursor-pointer" />
            <div className="flex items-center gap-1 cursor-pointer">
              <ShoppingBag className="h-5 w-5 text-gray-700" />
              <span className="text-sm text-gray-700">$0.00</span>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-4">
          <ul className="flex items-center gap-6 text-sm font-medium">
            <li className="text-red-600 font-semibold">SALE</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Men's</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Women's</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Kids</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Accessories</li>
            <li className="text-teal-600 hover:text-teal-700 cursor-pointer">Only at JD</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Brands</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Collections</li>
            <li className="text-blue-600 hover:text-blue-700 cursor-pointer">New</li>
            <li className="text-gray-700 hover:text-black cursor-pointer">Explore</li>
          </ul>
        </nav>
      </div>

      {/* Promotional banner */}
      <div className="bg-yellow-400 py-3">
        <div className="flex items-center justify-between px-4 text-sm font-medium text-black">
          <span>FREE DELIVERY FROM $50</span>
          <span className="flex items-center gap-2">
            10% CASHBACK ON FIRST PURCHASE WITH 🔋 STATUS
          </span>
          <span>PERFECT GIFT? JD GIFT CARD</span>
        </div>
      </div>
    </header>
  )
}
